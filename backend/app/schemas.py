from pydantic import BaseModel
from typing import List, Optional, Any, Dict
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
    source: str = "SIMULATION"
    razorpay_order_id: Optional[str] = None
    razorpay_payment_id: Optional[str] = None
    payment_provider: str = "Razorpay Test Mode"

class TransactionCreate(TransactionBase):
    pass

class RiskAssessmentResponse(BaseModel):
    risk_score: int
    risk_level: str
    signals: List[str]
    
    class Config:
        from_attributes = True
        orm_mode = True

class RecoveryAssessmentResponse(BaseModel):
    recovery_score: int
    recommended_action: str
    expected_recovery_probability: float
    expected_recovered_value: float
    
    class Config:
        from_attributes = True
        orm_mode = True

class AgentDecisionResponse(BaseModel):
    decision: str
    confidence: float
    reasoning: str
    
    class Config:
        from_attributes = True
        orm_mode = True

class PolicyEvaluationResponse(BaseModel):
    policy_decision: str
    policy_reason: str
    approved_action: str
    policy_rules: List[str]
    policy_evaluated_at: datetime
    
    class Config:
        from_attributes = True
        orm_mode = True

class RecoveryActionResponse(BaseModel):
    action_type: str
    status: str
    amount_recovered: float
    executed_at: datetime
    policy_evaluation: Optional[List[Dict[str, Any]]] = None
    
    class Config:
        from_attributes = True
        orm_mode = True

class AuditLogResponse(BaseModel):
    event_type: str
    actor: str
    details: Dict[str, Any]
    timestamp: datetime
    
    class Config:
        from_attributes = True
        orm_mode = True

class TransactionDetail(BaseModel):
    id: str
    amount: float
    currency: str
    payment_method: str
    status: str
    failure_reason: str
    device_id: str
    ip_address: str
    location: str
    source: str
    razorpay_order_id: Optional[str] = None
    razorpay_payment_id: Optional[str] = None
    payment_provider: str
    created_at: datetime
    
    risk_assessment: Optional[RiskAssessmentResponse] = None
    recovery_assessment: Optional[RecoveryAssessmentResponse] = None
    agent_decision: Optional[AgentDecisionResponse] = None
    policy_evaluation: Optional[PolicyEvaluationResponse] = None
    recovery_action: Optional[RecoveryActionResponse] = None
    audit_logs: List[AuditLogResponse] = []
    
    class Config:
        from_attributes = True
        orm_mode = True

class TrendPoint(BaseModel):
    date: str
    value: float

class DashboardMetrics(BaseModel):
    revenue_at_risk: float
    revenue_recovered: float
    recovery_rate: float
    unsafe_prevented: int
    high_risk_txns: int
    human_escalations: int
    policy_blocks: int = 0
    total_analyzed: int
    razorpay_count: int = 0
    simulated_count: int = 0
    revenue_trend: List[Dict[str, Any]] = []
    recovery_by_reason: List[Dict[str, Any]] = []
    risk_distribution: List[Dict[str, Any]] = []
    ai_actions: List[Dict[str, Any]] = []


class OrderCreateRequest(BaseModel):
    amount: float
    currency: str = "INR"
    receipt: Optional[str] = None

class OrderResponse(BaseModel):
    order_id: str
    amount: float
    currency: str
    key_id: str

class PaymentVerifyRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
