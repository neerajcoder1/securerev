from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, JSON, Text
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
