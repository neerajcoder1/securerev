import os
import random
import uuid
import sys

# Add backend to path so we can import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Transaction, Customer, Merchant, RiskAssessment, AgentDecision, AuditLog
from app.services import process_transaction

# Use local SQLite for this standalone run
engine = create_engine("sqlite:///./local_demo.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

def main():
    db = SessionLocal()
    
    # Ensure merchant exists
    if not db.query(Merchant).first():
        m = Merchant(name="Hackathon Merchant", email="demo@securerev.com", hashed_password="fake")
        db.add(m)
        db.commit()
    
    print("\n" + "="*60)
    print(" SECUREREV - RUNNING SIMULATION BATCH")
    print("="*60 + "\n")
    
    reasons = ["Network timeout", "Insufficient funds", "Bank rejected", "Fraud suspected"]
    devices = ["device_1 (Known)", "unknown_device (New)"]
    
    for i in range(10):
        # Generate random transaction
        amt = random.choice([500, 1500, 2500, 12000, 55000])
        reason = random.choice(reasons)
        device = random.choice(devices)
        ext_cust_id = f"CUST_{random.randint(100, 999)}"
        
        # Customer logic
        cust = db.query(Customer).filter(Customer.external_customer_id == ext_cust_id).first()
        if not cust:
            cust = Customer(merchant_id=1, external_customer_id=ext_cust_id)
            db.add(cust)
            db.commit()
            db.refresh(cust)
            
        txn_id = f"TXN_{uuid.uuid4().hex[:8].upper()}"
        
        db_txn = Transaction(
            id=txn_id,
            merchant_id=1,
            customer_id=cust.id,
            amount=amt,
            currency="INR",
            payment_method="UPI",
            status="FAILED",
            failure_reason=reason,
            device_id=device,
            ip_address="192.168.1.1",
            location="IN"
        )
        db.add(db_txn)
        db.commit()
        db.refresh(db_txn)
        
        # Run SecureRev Logic!
        process_transaction(db, db_txn)
        db.refresh(db_txn)
        
        # Retrieve results
        risk = db.query(RiskAssessment).filter_by(transaction_id=txn_id).first()
        decision = db.query(AgentDecision).filter_by(transaction_id=txn_id).first()
        
        # Print fancy output
        print(f"[{i+1}/10] Transaction: {txn_id} | Amount: ₹{amt:,}")
        print(f"       Failure: {reason} | Device: {device}")
        
        risk_color = "[HIGH]" if risk.risk_level == "HIGH" else ("[MED]" if risk.risk_level == "MEDIUM" else "[LOW]")
        print(f"       Risk Assessment: {risk_color} {risk.risk_level} (Score: {risk.risk_score})")
        if risk.signals:
            print(f"       Flags: {', '.join(risk.signals)}")
            
        print(f"       AI Decision: [AI] {decision.decision} (Confidence: {decision.confidence*100:.0f}%)")
        print(f"       AI Reasoning: {decision.reasoning}")
        
        status_color = "[OK]" if db_txn.status == "RECOVERED" else ("[ESC]" if db_txn.status == "ESCALATED" else "[FAIL]")
        print(f"       Final Result: {status_color} {db_txn.status}\n")

    
    # Print metrics
    txns = db.query(Transaction).all()
    recovered = sum(t.amount for t in txns if t.status == "RECOVERED")
    prevented = db.query(AgentDecision).filter(AgentDecision.decision == "ESCALATE_TO_HUMAN").count()
    
    print("="*60)
    print("📊 SIMULATION METRICS")
    print("="*60)
    print(f"Total Transactions Processed : {len(txns)}")
    print(f"Revenue Successfully Recovered: ₹{recovered:,.2f}")
    print(f"Unsafe Actions Prevented     : {prevented}")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
