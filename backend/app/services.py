import random
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
