import os

files = {
    "backend/app/__init__.py": "",
    
    "backend/app/config.py": """import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "securerev")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "securerev_dev_pass")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "securerev")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "postgres") # defaults to docker-compose service name
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings()
""",
    
    "backend/app/database.py": """from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
import time

# Added retry logic for database connection during startup
engine = None
for i in range(5):
    try:
        engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
        engine.connect()
        break
    except Exception as e:
        time.sleep(2)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""",
    
    "backend/app/models.py": """from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, JSON, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Merchant(Base):
    __tablename__ = "merchants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    merchant_id = Column(Integer, ForeignKey("merchants.id"))
    external_customer_id = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(String, primary_key=True, index=True)
    merchant_id = Column(Integer, ForeignKey("merchants.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    amount = Column(Float, nullable=False)
    currency = Column(String, default="INR")
    payment_method = Column(String)
    status = Column(String)
    failure_reason = Column(String)
    device_id = Column(String)
    ip_address = Column(String)
    location = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    risk_assessment = relationship("RiskAssessment", back_populates="transaction", uselist=False)
    recovery_assessment = relationship("RecoveryAssessment", back_populates="transaction", uselist=False)
    agent_decision = relationship("AgentDecision", back_populates="transaction", uselist=False)

class RiskAssessment(Base):
    __tablename__ = "risk_assessments"
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, ForeignKey("transactions.id"))
    risk_score = Column(Integer)
    risk_level = Column(String)
    signals = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    transaction = relationship("Transaction", back_populates="risk_assessment")

class RecoveryAssessment(Base):
    __tablename__ = "recovery_assessments"
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, ForeignKey("transactions.id"))
    recovery_score = Column(Integer)
    recommended_action = Column(String)
    expected_recovery_probability = Column(Float)
    expected_recovered_value = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    transaction = relationship("Transaction", back_populates="recovery_assessment")

class AgentDecision(Base):
    __tablename__ = "agent_decisions"
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, ForeignKey("transactions.id"))
    decision = Column(String)
    confidence = Column(Float)
    reasoning = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    transaction = relationship("Transaction", back_populates="agent_decision")

class RecoveryAction(Base):
    __tablename__ = "recovery_actions"
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, ForeignKey("transactions.id"))
    action_type = Column(String)
    status = Column(String)
    amount_recovered = Column(Float, default=0.0)
    executed_at = Column(DateTime(timezone=True), server_default=func.now())

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, ForeignKey("transactions.id"))
    event_type = Column(String)
    actor = Column(String)
    details = Column(JSON)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
""",
    
    "backend/app/schemas.py": """from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

class TransactionBase(BaseModel):
    amount: float
    currency: str = "INR"
    payment_method: str
    status: str
    failure_reason: str
    device_id: str
    ip_address: str
    location: str
    customer_external_id: str

class TransactionCreate(TransactionBase):
    pass

class RiskAssessmentResponse(BaseModel):
    risk_score: int
    risk_level: str
    signals: List[str]

class RecoveryAssessmentResponse(BaseModel):
    recovery_score: int
    recommended_action: str
    expected_recovery_probability: float
    expected_recovered_value: float

class AgentDecisionResponse(BaseModel):
    decision: str
    confidence: float
    reasoning: str

class TransactionDetail(BaseModel):
    id: str
    amount: float
    status: str
    failure_reason: str
    created_at: datetime
    risk_assessment: Optional[RiskAssessmentResponse] = None
    recovery_assessment: Optional[RecoveryAssessmentResponse] = None
    agent_decision: Optional[AgentDecisionResponse] = None
    
    class Config:
        orm_mode = True

class DashboardMetrics(BaseModel):
    revenue_at_risk: float
    revenue_recovered: float
    recovery_rate: float
    unsafe_prevented: int
    high_risk_txns: int
    human_escalations: int
""",
    
    "backend/app/services.py": """import random
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from app.models import Transaction, RiskAssessment, RecoveryAssessment, AgentDecision, AuditLog, RecoveryAction
from datetime import datetime

class SecurityEngine:
    @staticmethod
    def analyze(db: Session, txn: Transaction) -> Dict[str, Any]:
        score = 10
        signals = []
        if txn.amount > 10000:
            score += 40
            signals.append("High amount anomaly")
        if txn.device_id == "unknown_device":
            score += 30
            signals.append("Unrecognized device")
        if random.random() > 0.8:
            score += 20
            signals.append("Payment method switching detected")
            
        level = "LOW"
        if score > 75: level = "HIGH"
        elif score > 40: level = "MEDIUM"
        
        return {"risk_score": min(score, 100), "risk_level": level, "signals": signals}

class RecoveryEngine:
    @staticmethod
    def analyze(db: Session, txn: Transaction) -> Dict[str, Any]:
        base_prob = 0.8 if txn.failure_reason in ["Network timeout", "Temporary hold"] else 0.4
        if txn.amount > 5000: base_prob -= 0.2
        
        score = int(base_prob * 100)
        action = "RETRY_PAYMENT" if score > 70 else "GENERATE_PAYMENT_LINK"
        return {
            "recovery_score": score,
            "recommended_action": action,
            "expected_recovery_probability": base_prob,
            "expected_recovered_value": txn.amount * base_prob
        }

class AgentService:
    @staticmethod
    def decide(risk: Dict, recovery: Dict, txn: Transaction) -> Dict[str, Any]:
        if risk['risk_score'] > 75:
            return {"decision": "ESCALATE_TO_HUMAN", "confidence": 0.95, "reasoning": "High security risk overrides recovery."}
        if recovery['recovery_score'] > 70:
            return {"decision": "RETRY_PAYMENT", "confidence": 0.88, "reasoning": "Low risk and high recovery probability."}
        return {"decision": "GENERATE_PAYMENT_LINK", "confidence": 0.75, "reasoning": "Moderate recovery chance, safer via async link."}

class PolicyEngine:
    @staticmethod
    def evaluate(decision: str, risk_score: int, amount: float) -> str:
        if decision == "RETRY_PAYMENT" and risk_score > 50:
            return "ESCALATE_TO_HUMAN"
        if decision == "RETRY_PAYMENT" and amount > 50000:
            return "ESCALATE_TO_HUMAN"
        return decision

class RazorpayService:
    @staticmethod
    def execute_action(action: str, txn: Transaction) -> bool:
        if action == "RETRY_PAYMENT":
            return True # Mock success
        return False

def process_transaction(db: Session, txn: Transaction):
    risk = SecurityEngine.analyze(db, txn)
    db_risk = RiskAssessment(transaction_id=txn.id, **risk)
    db.add(db_risk)
    
    rec = RecoveryEngine.analyze(db, txn)
    db_rec = RecoveryAssessment(transaction_id=txn.id, **rec)
    db.add(db_rec)
    
    decision = AgentService.decide(risk, rec, txn)
    db_dec = AgentDecision(transaction_id=txn.id, **decision)
    db.add(db_dec)
    
    final_action = PolicyEngine.evaluate(decision["decision"], risk["risk_score"], txn.amount)
    
    success = False
    if final_action in ["RETRY_PAYMENT", "GENERATE_PAYMENT_LINK"]:
        success = RazorpayService.execute_action(final_action, txn)
        txn.status = "RECOVERED" if success else "FAILED"
        if final_action == "ESCALATE_TO_HUMAN":
            txn.status = "ESCALATED"
    else:
        txn.status = "FAILED" if final_action == "NO_ACTION" else "ESCALATED"
        
    action_log = RecoveryAction(transaction_id=txn.id, action_type=final_action, status="SUCCESS" if success else "PENDING", amount_recovered=txn.amount if success else 0)
    db.add(action_log)
    
    db.add(AuditLog(transaction_id=txn.id, event_type="RECOVERY_ATTEMPTED", actor="SYSTEM", details={"action": final_action, "success": success}))
    db.commit()
""",
    
    "backend/app/routers.py": """from fastapi import APIRouter, Depends, HTTPException
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
""",
    
    "backend/app/main.py": """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, SessionLocal
from app.routers import router
from app.models import Merchant
from passlib.context import CryptContext

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SecureRev API", description="Autonomous Secure Revenue Recovery Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not db.query(Merchant).first():
        m = Merchant(name="Demo Merchant", email="demo@securerev.com", hashed_password=pwd_context.hash("demo"))
        db.add(m)
        db.commit()
    db.close()
""",

    "frontend/components/Sidebar.tsx": """import Link from 'next/link'
import { LayoutDashboard, Receipt, Activity } from 'lucide-react'

export default function Sidebar() {
  return (
    <div className="w-64 bg-slate-900 text-white min-h-screen p-4">
      <div className="text-2xl font-bold mb-8 text-blue-400">SecureRev</div>
      <nav className="space-y-4">
        <Link href="/" className="flex items-center space-x-2 p-2 hover:bg-slate-800 rounded">
          <LayoutDashboard size={20} /> <span>Dashboard</span>
        </Link>
        <Link href="/transactions" className="flex items-center space-x-2 p-2 hover:bg-slate-800 rounded">
          <Receipt size={20} /> <span>Transactions</span>
        </Link>
        <Link href="/agent" className="flex items-center space-x-2 p-2 hover:bg-slate-800 rounded">
          <Activity size={20} /> <span>Agent Activity</span>
        </Link>
      </nav>
    </div>
  )
}
""",

    "frontend/app/layout.tsx": """import './globals.css'
import Sidebar from '../components/Sidebar'

export const metadata = {
  title: 'SecureRev',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="flex bg-gray-50 text-gray-900">
        <Sidebar />
        <main className="flex-1 p-8 overflow-y-auto h-screen">
          {children}
        </main>
      </body>
    </html>
  )
}
""",

    "frontend/app/page.tsx": """"use client"
import { useEffect, useState } from 'react'

export default function Dashboard() {
  const [metrics, setMetrics] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const fetchMetrics = () => {
    fetch('http://localhost:8000/api/v1/dashboard/metrics')
      .then(r => r.json())
      .then(d => setMetrics(d))
      .catch(e => console.error(e))
  }

  useEffect(() => { fetchMetrics() }, [])

  const simulate = async () => {
    setLoading(true)
    await fetch('http://localhost:8000/api/v1/simulate', { method: 'POST' })
    fetchMetrics()
    setLoading(false)
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Revenue Recovery Dashboard</h1>
        <button onClick={simulate} disabled={loading} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          {loading ? 'Simulating...' : 'Run Simulation'}
        </button>
      </div>
      
      {metrics ? (
        <div className="grid grid-cols-4 gap-4 mb-8">
          <div className="bg-white p-6 rounded shadow border-l-4 border-red-500">
            <div className="text-gray-500 text-sm">Revenue at Risk</div>
            <div className="text-2xl font-bold text-red-600">₹{metrics.revenue_at_risk.toLocaleString()}</div>
          </div>
          <div className="bg-white p-6 rounded shadow border-l-4 border-green-500">
            <div className="text-gray-500 text-sm">Revenue Recovered</div>
            <div className="text-2xl font-bold text-green-600">₹{metrics.revenue_recovered.toLocaleString()}</div>
          </div>
          <div className="bg-white p-6 rounded shadow border-l-4 border-blue-500">
            <div className="text-gray-500 text-sm">Recovery Rate</div>
            <div className="text-2xl font-bold text-blue-600">{metrics.recovery_rate.toFixed(1)}%</div>
          </div>
          <div className="bg-white p-6 rounded shadow border-l-4 border-orange-500">
            <div className="text-gray-500 text-sm">Unsafe Prevented</div>
            <div className="text-2xl font-bold text-orange-600">{metrics.unsafe_prevented}</div>
          </div>
        </div>
      ) : (
        <p>Loading metrics... Make sure backend is running.</p>
      )}
    </div>
  )
}
""",

    "frontend/app/transactions/page.tsx": """"use client"
import { useEffect, useState } from 'react'

export default function Transactions() {
  const [txns, setTxns] = useState<any[]>([])

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/transactions')
      .then(r => r.json())
      .then(d => setTxns(d))
      .catch(e => console.error(e))
  }, [])

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Transaction Explorer</h1>
      <div className="bg-white rounded shadow overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-100">
            <tr>
              <th className="p-4">ID</th>
              <th className="p-4">Amount</th>
              <th className="p-4">Failure Reason</th>
              <th className="p-4">Status</th>
              <th className="p-4">Risk Level</th>
              <th className="p-4">AI Decision</th>
            </tr>
          </thead>
          <tbody>
            {txns.map(t => (
              <tr key={t.id} className="border-t">
                <td className="p-4 font-mono text-sm">{t.id}</td>
                <td className="p-4 font-semibold">₹{t.amount}</td>
                <td className="p-4 text-red-500">{t.failure_reason}</td>
                <td className="p-4">
                  <span className={`px-2 py-1 rounded text-xs ${t.status === 'RECOVERED' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {t.status}
                  </span>
                </td>
                <td className="p-4">{t.risk_assessment?.risk_level || 'N/A'}</td>
                <td className="p-4">{t.agent_decision?.decision || 'N/A'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
""",

    "frontend/app/agent/page.tsx": """"use client"
import { useEffect, useState } from 'react'

export default function AgentActivity() {
  const [activity, setActivity] = useState<any[]>([])

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/agent/activity')
      .then(r => r.json())
      .then(d => setActivity(d))
      .catch(e => console.error(e))
  }, [])

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Live Agent Activity</h1>
      <div className="space-y-4">
        {activity.map((a, i) => (
          <div key={i} className="bg-white p-4 rounded shadow border-l-4 border-blue-500 flex flex-col">
            <div className="flex justify-between mb-2">
              <span className="font-bold text-gray-800">{a.decision}</span>
              <span className="font-mono text-sm text-gray-500">{a.transaction_id}</span>
            </div>
            <p className="text-gray-600">{a.reasoning}</p>
            <span className="text-xs text-gray-400 mt-2">{new Date(a.timestamp).toLocaleString()}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
"""
}

for rel_path, content in files.items():
    full_path = os.path.join(r"C:\Users\HP\OneDrive\Desktop\backend\securerev", rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Codebase successfully generated!")
