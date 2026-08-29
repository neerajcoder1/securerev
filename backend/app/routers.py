from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
import random
from app.database import get_db
from app.models import Transaction, Customer, Merchant, AuditLog, RiskAssessment, AgentDecision
from app.schemas import TransactionCreate, TransactionDetail, DashboardMetrics
from app.services import process_transaction

router = APIRouter()

@router.post("/transactions", response_model=TransactionDetail)
def create_transaction(txn_in: TransactionCreate, db: Session = Depends(get_db)):
    cust = db.query(Customer).filter(Customer.external_customer_id == txn_in.customer_external_id).first()
    if not cust:
        cust = Customer(merchant_id=1, external_customer_id=txn_in.customer_external_id)
        db.add(cust)
        db.commit()
        db.refresh(cust)
        
    txn_id = f"TXN_{uuid.uuid4().hex[:8].upper()}"
    db_txn = Transaction(
        id=txn_id,
        merchant_id=1,
        customer_id=cust.id,
        amount=txn_in.amount,
        currency=txn_in.currency,
        payment_method=txn_in.payment_method,
        status=txn_in.status,
        failure_reason=txn_in.failure_reason,
        device_id=txn_in.device_id,
        ip_address=txn_in.ip_address,
        location=txn_in.location
    )
    db.add(db_txn)
    db.flush()
    db.add(AuditLog(transaction_id=txn_id, event_type="TRANSACTION_CREATED", actor="SYSTEM", details={}))
    db.commit()
    db.refresh(db_txn)
    
    process_transaction(db, db_txn)
    db.refresh(db_txn)
    return db_txn

@router.get("/transactions", response_model=List[TransactionDetail])
def get_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).order_by(Transaction.created_at.desc()).limit(50).all()

@router.get("/dashboard/metrics", response_model=DashboardMetrics)
def get_metrics(db: Session = Depends(get_db)):
    txns = db.query(Transaction).all()
    recovered = sum(t.amount for t in txns if t.status == "RECOVERED")
    at_risk = sum(t.amount for t in txns if t.status in ["FAILED", "ESCALATED"]) + recovered
    
    high_risk = db.query(RiskAssessment).filter(RiskAssessment.risk_level == "HIGH").count()
    prevented = db.query(AgentDecision).filter(AgentDecision.decision == "ESCALATE_TO_HUMAN").count()
    
    return DashboardMetrics(
        revenue_at_risk=at_risk,
        revenue_recovered=recovered,
        recovery_rate=(recovered / at_risk * 100) if at_risk > 0 else 0,
        unsafe_prevented=prevented,
        high_risk_txns=high_risk,
        human_escalations=prevented
    )
    
@router.post("/simulate")
def run_simulation(db: Session = Depends(get_db)):
    reasons = ["Network timeout", "Insufficient funds", "Bank rejected"]
    devices = ["device_1", "unknown_device"]
    for i in range(10):
        amt = random.choice([500, 1500, 2500, 12000])
        txn_in = TransactionCreate(
            amount=amt,
            payment_method="UPI",
            status="FAILED",
            failure_reason=random.choice(reasons),
            device_id=random.choice(devices),
            ip_address="192.168.1.1",
            location="IN",
            customer_external_id=f"CUST_{random.randint(100,999)}"
        )
        create_transaction(txn_in, db)
    return {"status": "Simulation completed"}

@router.get("/agent/activity")
def get_activity(db: Session = Depends(get_db)):
    decisions = db.query(AgentDecision).order_by(AgentDecision.created_at.desc()).limit(20).all()
    res = []
    for d in decisions:
        res.append({
            "transaction_id": d.transaction_id,
            "decision": d.decision,
            "reasoning": d.reasoning,
            "timestamp": d.created_at
        })
    return res
