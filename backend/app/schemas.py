from pydantic import BaseModel
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
