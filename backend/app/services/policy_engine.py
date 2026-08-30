class PolicyEngine:
    MAX_AUTO_RETRIES = 1
    MAX_SECURITY_RISK = 70
    MIN_RECOVERY_SCORE = 50
    MAX_AUTO_RECOVERY_AMOUNT = 10000

    @classmethod
    def evaluate(cls, ai_decision: str, security_risk: int, recovery_score: int, retry_count: int, transaction_amount: float) -> dict:
        rules_evaluated = [
            "security_risk_limit",
            "recovery_score_limit",
            "retry_limit",
            "transaction_amount_limit"
        ]
        
        if security_risk >= cls.MAX_SECURITY_RISK:
            return {
                "policy_decision": "BLOCKED",
                "approved_action": "ESCALATE_TO_HUMAN",
                "reason": f"Security risk ({security_risk}) exceeds maximum automatic recovery limit ({cls.MAX_SECURITY_RISK}).",
                "rules_evaluated": ["security_risk_limit"]
            }
            
        if recovery_score < cls.MIN_RECOVERY_SCORE:
            return {
                "policy_decision": "BLOCKED",
                "approved_action": "NO_ACTION",
                "reason": f"Recovery score ({recovery_score}) is below minimum threshold ({cls.MIN_RECOVERY_SCORE}).",
                "rules_evaluated": ["recovery_score_limit"]
            }
            
        if retry_count >= cls.MAX_AUTO_RETRIES and ai_decision == "RETRY_PAYMENT":
            return {
                "policy_decision": "BLOCKED",
                "approved_action": "ESCALATE_TO_HUMAN",
                "reason": f"Retry limit ({cls.MAX_AUTO_RETRIES}) reached.",
                "rules_evaluated": ["retry_limit"]
            }
            
        if transaction_amount > cls.MAX_AUTO_RECOVERY_AMOUNT and ai_decision != "NO_ACTION":
            return {
                "policy_decision": "BLOCKED",
                "approved_action": "ESCALATE_TO_HUMAN",
                "reason": f"Transaction amount (?{transaction_amount}) exceeds maximum automatic recovery amount (?{cls.MAX_AUTO_RECOVERY_AMOUNT}).",
                "rules_evaluated": ["transaction_amount_limit"]
            }
            
        return {
            "policy_decision": "APPROVED",
            "approved_action": ai_decision,
            "reason": "All safety thresholds passed. AI recommendation approved.",
            "rules_evaluated": rules_evaluated
        }
