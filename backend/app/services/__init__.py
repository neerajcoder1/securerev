import random
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from app.models import Transaction, RiskAssessment, RecoveryAssessment, AgentDecision, AuditLog, RecoveryAction, PolicyEvaluation
from datetime import datetime
from app.services.policy_engine import PolicyEngine

class SecurityEngine:
    @staticmethod
    def analyze(db: Session, txn: Transaction) -> Dict[str, Any]:
        score = 10
        signals = ["Normal account age", "Normal location"]
        if txn.amount > 10000:
            score += 40
            signals.append("High amount anomaly")
        if txn.device_id == "unknown_device":
            score += 30
            signals.append("Unrecognized device detected")
        if txn.failure_reason == "Bank rejected" or random.random() > 0.8:
            score += 20
            signals.append("Multiple payment methods/failures detected")
            
        level = "LOW"
        if score > 75: level = "HIGH"
        elif score > 40: level = "MEDIUM"
        
        return {"risk_score": min(score, 100), "risk_level": level, "signals": signals}

class RecoveryEngine:
    @staticmethod
    def analyze(db: Session, txn: Transaction) -> Dict[str, Any]:
        base_prob = 0.8 if txn.failure_reason in ["Network timeout", "Temporary hold"] else 0.4
        if txn.amount > 5000: base_prob -= 0.1
        if txn.failure_reason == "Insufficient funds": base_prob = 0.6
        
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
        # AI no longer enforces hard policy limits. It makes recommendations based on patterns.
        if txn.failure_reason == "Repeated failure":
            return {"decision": "NO_ACTION", "confidence": 0.99, "reasoning": "Repeated failures indicate unrecoverable transaction."}
            
        if recovery['recovery_score'] >= 70:
            return {"decision": "RETRY_PAYMENT", "confidence": 0.88, "reasoning": "Temporary network timeout detected. Customer has a strong successful-payment history and no significant security anomalies."}
            
        return {"decision": "GENERATE_PAYMENT_LINK", "confidence": 0.75, "reasoning": "Customer has a strong payment history but current failure indicates insufficient funds. Async link is safer."}

class RazorpayService:
    @staticmethod
    def execute_action(action: str, txn: Transaction) -> bool:
        if action == "RETRY_PAYMENT":
            return True # Mock success
        return False

def process_transaction(db: Session, txn: Transaction):
    # 1. Security Analysis
    risk = SecurityEngine.analyze(db, txn)
    db_risk = RiskAssessment(transaction_id=txn.id, **risk)
    db.add(db_risk)
    db.flush()
    db.add(AuditLog(transaction_id=txn.id, event_type="SECURITY_ANALYSIS_COMPLETED", actor="SYSTEM", details=risk))
    
    # 2. Recovery Analysis
    rec = RecoveryEngine.analyze(db, txn)
    db_rec = RecoveryAssessment(transaction_id=txn.id, **rec)
    db.add(db_rec)
    db.flush()
    db.add(AuditLog(transaction_id=txn.id, event_type="RECOVERY_ANALYSIS_COMPLETED", actor="SYSTEM", details=rec))
    
    # 3. AI Decision
    decision = AgentService.decide(risk, rec, txn)
    db_dec = AgentDecision(transaction_id=txn.id, **decision)
    db.add(db_dec)
    db.flush()
    db.add(AuditLog(transaction_id=txn.id, event_type="AI_DECISION_GENERATED", actor="SYSTEM", details=decision))
    
    # 4. Policy Engine Evaluation
    # Using dummy retry_count = 0 for now unless we track it
    retry_count = 0 
    if txn.failure_reason == 'Repeated failure':
        retry_count = 1
        
    policy_result = PolicyEngine.evaluate(
        ai_decision=decision["decision"], 
        security_risk=risk["risk_score"], 
        recovery_score=rec["recovery_score"], 
        retry_count=retry_count, 
        transaction_amount=txn.amount
    )
    
    final_action = policy_result["approved_action"]
    
    db_policy = PolicyEvaluation(
        transaction_id=txn.id,
        policy_decision=policy_result["policy_decision"],
        policy_reason=policy_result["reason"],
        approved_action=final_action,
        policy_rules=policy_result["rules_evaluated"]
    )
    db.add(db_policy)
    db.flush()
    
    # Detailed Audit Logging for Policy
    audit_details = {
        "AI_decision": decision["decision"],
        "security_risk": risk["risk_score"],
        "recovery_score": rec["recovery_score"],
        "policy_decision": policy_result["policy_decision"],
        "approved_action": final_action,
        "rules_evaluated": policy_result["rules_evaluated"],
        "reason": policy_result["reason"]
    }
    db.add(AuditLog(transaction_id=txn.id, event_type="POLICY_EVALUATED", actor="SYSTEM", details=audit_details))
    if policy_result["policy_decision"] == "APPROVED":
        db.add(AuditLog(transaction_id=txn.id, event_type="POLICY_APPROVED", actor="SYSTEM", details={"action": final_action}))
    else:
        db.add(AuditLog(transaction_id=txn.id, event_type="POLICY_BLOCKED", actor="SYSTEM", details={"reason": policy_result["reason"], "fallback_action": final_action}))
        
    # 5. Recovery Service Execution
    success = False
    if final_action in ["RETRY_PAYMENT", "GENERATE_PAYMENT_LINK"]:
        success = RazorpayService.execute_action(final_action, txn)
        txn.status = "RECOVERED" if success else "FAILED"
    else:
        txn.status = "FAILED" if final_action == "NO_ACTION" else "ESCALATED"
        
    action_log = RecoveryAction(
        transaction_id=txn.id, 
        action_type=final_action, 
        status="SUCCESS" if success else "PENDING", 
        amount_recovered=txn.amount if success else 0
    )
    db.add(action_log)
    db.flush()
    
    db.add(AuditLog(transaction_id=txn.id, event_type="RECOVERY_ACTION_EXECUTED", actor="SYSTEM", details={"action": final_action, "success": success}))
    
    if success:
        db.add(AuditLog(transaction_id=txn.id, event_type="PAYMENT_RECOVERED", actor="SYSTEM", details={"amount": txn.amount}))
        
    db.commit()
