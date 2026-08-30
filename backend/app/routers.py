from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import uuid
import random
from datetime import datetime, timedelta
from app.database import get_db
from app.models import PolicyEvaluation, Transaction, Customer, Merchant, AuditLog, RiskAssessment, AgentDecision, RecoveryAssessment
from app.schemas import TransactionCreate, TransactionDetail, DashboardMetrics, TrendPoint, OrderCreateRequest, OrderResponse, PaymentVerifyRequest
from app.services import process_transaction
from app.razorpay_service import razorpay_client
from fastapi import Request, BackgroundTasks

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

@router.get("/transactions/{txn_id}", response_model=TransactionDetail)
def get_transaction(txn_id: str, db: Session = Depends(get_db)):
    txn = db.query(Transaction).filter(Transaction.id == txn_id).first()
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return txn

@router.get("/dashboard/metrics", response_model=DashboardMetrics)
def get_metrics(db: Session = Depends(get_db)):
    txns = db.query(Transaction).all()
    total_analyzed = len(txns)
    razorpay_count = sum(1 for t in txns if t.source == "RAZORPAY TEST")
    simulated_count = total_analyzed - razorpay_count
    recovered = sum(t.amount for t in txns if t.status == "RECOVERED")
    at_risk = sum(t.amount for t in txns if t.status in ["FAILED", "ESCALATED"]) + recovered
    
    high_risk = db.query(RiskAssessment).filter(RiskAssessment.risk_level == "HIGH").count()
    prevented = db.query(AgentDecision).filter(AgentDecision.decision == "ESCALATE_TO_HUMAN").count()
    policy_blocks = db.query(PolicyEvaluation).filter(PolicyEvaluation.policy_decision == "BLOCKED").count()
    
    # Trends mock data for charts
    base_date = datetime.now() - timedelta(days=6)
    revenue_trend = []
    for i in range(7):
        d = (base_date + timedelta(days=i)).strftime("%b %d")
        revenue_trend.append({"date": d, "value": random.randint(1000, 15000)})
        
    risk_dist = [
        {"name": "LOW", "value": db.query(RiskAssessment).filter(RiskAssessment.risk_level == "LOW").count()},
        {"name": "MEDIUM", "value": db.query(RiskAssessment).filter(RiskAssessment.risk_level == "MEDIUM").count()},
        {"name": "HIGH", "value": high_risk}
    ]
    
    # Recovery by reason
    reasons = {}
    for t in txns:
        if t.failure_reason not in reasons:
            reasons[t.failure_reason] = 0
        reasons[t.failure_reason] += 1
    recovery_by_reason = [{"name": k, "value": v} for k, v in reasons.items()]
    
    # AI Actions
    actions = {}
    for a in db.query(AgentDecision).all():
        if a.decision not in actions:
            actions[a.decision] = 0
        actions[a.decision] += 1
    ai_actions = [{"name": k, "value": v} for k, v in actions.items()]
    
    return DashboardMetrics(
        revenue_at_risk=at_risk,
        revenue_recovered=recovered,
        recovery_rate=(recovered / at_risk * 100) if at_risk > 0 else 0,
        unsafe_prevented=prevented,
        high_risk_txns=high_risk,
        human_escalations=prevented,
        policy_blocks=policy_blocks,
        total_analyzed=total_analyzed,
        razorpay_count=razorpay_count,
        simulated_count=simulated_count,
        revenue_trend=revenue_trend,
        risk_distribution=risk_dist,
        recovery_by_reason=recovery_by_reason,
        ai_actions=ai_actions
    )
    
@router.post("/simulate")
def run_simulation(db: Session = Depends(get_db)):
    scenarios = [
        # Scenario 1: Temporary Network Timeout (Expected: Retry)
        {"amount": 1500, "failure_reason": "Network timeout", "device_id": "known_device"},
        # Scenario 2: Insufficient Funds (Expected: Payment Link)
        {"amount": 2500, "failure_reason": "Insufficient funds", "device_id": "known_device"},
        # Scenario 3: High Risk (Expected: Escalate)
        {"amount": 12000, "failure_reason": "Bank rejected", "device_id": "unknown_device"},
        # Scenario 4: Repeated Failure (Expected: No Action)
        {"amount": 500, "failure_reason": "Repeated failure", "device_id": "known_device"},
        # Scenario 5: Normal Recovery
        {"amount": 3500, "failure_reason": "Network timeout", "device_id": "known_device"}
    ]
    
    for s in scenarios:
        txn_in = TransactionCreate(
            amount=s["amount"],
            payment_method="UPI",
            status="FAILED",
            failure_reason=s["failure_reason"],
            device_id=s["device_id"],
            ip_address="192.168.1.1",
            location="IN",
            customer_external_id=f"CUST_{random.randint(100,999)}"
        )
        create_transaction(txn_in, db)
        
    return {"status": "Simulation completed", "transactions_processed": len(scenarios)}

@router.get("/agent/activity")
def get_activity(db: Session = Depends(get_db)):
    decisions = db.query(AgentDecision).order_by(AgentDecision.created_at.desc()).limit(20).all()
    res = []
    for d in decisions:
        txn = d.transaction
        rec_score = txn.recovery_assessment.recovery_score if txn.recovery_assessment else 0
        risk_score = txn.risk_assessment.risk_score if txn.risk_assessment else 0
        pol = txn.policy_evaluation
        res.append({
            "transaction_id": d.transaction_id,
            "decision": d.decision,
            "reasoning": d.reasoning,
            "timestamp": d.created_at,
            "recovery_score": rec_score,
            "security_risk": risk_score,
            "policy_decision": pol.policy_decision if pol else "N/A",
            "policy_reason": pol.policy_reason if pol else "",
            "approved_action": pol.approved_action if pol else d.decision,
            "policy_rules": len(pol.policy_rules) if pol and pol.policy_rules else 0,
            "result": txn.status,
            "amount_recovered": txn.amount if txn.status == "RECOVERED" else 0
        })
    return res

@router.post("/payments/orders", response_model=OrderResponse)
def create_test_order(req: OrderCreateRequest, db: Session = Depends(get_db)):
    try:
        order = razorpay_client.create_order(amount=req.amount, currency=req.currency, receipt=req.receipt)
        return OrderResponse(
            order_id=order['id'],
            amount=req.amount,
            currency=req.currency,
            key_id=razorpay_client.key_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/payments/verify")
def verify_payment(req: PaymentVerifyRequest, db: Session = Depends(get_db)):
    is_valid = razorpay_client.verify_payment_signature(req.razorpay_order_id, req.razorpay_payment_id, req.razorpay_signature)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid signature")
    return {"status": "verified"}

@router.post("/webhooks/razorpay")
async def razorpay_webhook(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    signature = request.headers.get("X-Razorpay-Signature")
    if not signature:
        raise HTTPException(status_code=400, detail="Missing signature")
        
    payload = await request.body()
    is_valid = razorpay_client.verify_webhook_signature(payload.decode('utf-8'), signature)
    
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid webhook signature")
        
    data = await request.json()
    event = data.get("event")
    
    if event == "payment.failed":
        # Simulate processing the failed payment
        payload_data = data.get("payload", {}).get("payment", {}).get("entity", {})
        amt = payload_data.get("amount", 0) / 100.0
        reason = payload_data.get("error_description", "Unknown Error")
        order_id = payload_data.get("order_id")
        payment_id = payload_data.get("id")
        
        # Check idempotency
        existing = db.query(Transaction).filter(Transaction.razorpay_payment_id == payment_id).first()
        if existing:
            return {"status": "already processed"}
            
        txn_in = TransactionCreate(
            amount=amt,
            currency="INR",
            payment_method="CARD",
            status="FAILED",
            failure_reason=reason,
            device_id="webhook_device",
            ip_address="0.0.0.0",
            location="IN",
            customer_external_id="CUST_WEBHOOK",
            source="RAZORPAY TEST",
            razorpay_order_id=order_id,
            razorpay_payment_id=payment_id
        )
        # Process in background to avoid holding up the webhook response
        create_transaction(txn_in, db)
        
    return {"status": "ok"}

def create_transaction_task(txn_in, db):
    create_transaction(txn_in, db)


@router.post("/webhooks/local-demo")
def local_demo_webhook(request: dict, db: Session = Depends(get_db)):
    # Localhost bypass for hackathon presentations since webhooks can't reach localhost
    amt = request.get("amount", 0) / 100.0
    reason = request.get("error_description", "Unknown Error")
    payment_id = request.get("id", f"pay_mock_{random.randint(100,999)}")
    order_id = request.get("order_id", f"order_mock_{random.randint(100,999)}")
    
    txn_in = TransactionCreate(
        amount=amt,
        currency="INR",
        payment_method="CARD",
        status="FAILED",
        failure_reason=reason,
        device_id="webhook_device",
        ip_address="0.0.0.0",
        location="IN",
        customer_external_id="CUST_WEBHOOK",
        source="RAZORPAY TEST",
        razorpay_order_id=order_id,
        razorpay_payment_id=payment_id
    )
    create_transaction(txn_in, db)
    return {"status": "ok"}
