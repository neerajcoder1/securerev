# SecureRev — Autonomous Secure Revenue Recovery Agent

SecureRev is a B2B fintech platform designed to help merchants recover legitimate failed payments while preventing unsafe or suspicious transactions from being automatically recovered.

The system combines **Revenue Recovery Intelligence, Payment Security Intelligence, an AI Decision Agent, and a deterministic Policy Engine** to create a bounded autonomous recovery workflow.

> **Disclaimer:** SecureRev is a hackathon prototype. It does not represent a production integration with Razorpay. Razorpay interactions are performed in Test Mode or through controlled simulations. No real customer money is processed by the prototype.

---

# Dashboard

<img width="1887" height="876" alt="image" src="https://github.com/user-attachments/assets/cd274662-73e1-48d0-bb4f-ad67116c9c57" />

The Dashboard provides a merchant-level overview of revenue recovery performance.

It displays:

- Revenue at Risk
- Revenue Recovered
- Recovery Rate
- Unsafe Transactions Prevented
- Revenue Recovery Trend
- Security Risk Distribution
- Total Transactions
- Simulated and Razorpay Test transactions

The objective is to make the financial impact of the recovery agent immediately visible.

---

# Transactions

<img width="1860" height="874" alt="image" src="https://github.com/user-attachments/assets/32405555-14e6-463d-9ad6-ad4dad3d936a" />

The Transaction Explorer provides a transaction-level audit trail.

Each transaction contains:

- Transaction ID
- Transaction Amount
- Failure Reason
- Transaction Status
- Risk Level
- AI Decision
- Recovery Outcome

Example decisions include:

- `RETRY_PAYMENT`
- `GENERATE_PAYMENT_LINK`
- `NO_ACTION`
- `ESCALATE_TO_HUMAN`

This allows merchants to understand not only what happened, but also why the system selected a particular recovery action.

---

# Agent Activity

<img width="1863" height="876" alt="image" src="https://github.com/user-attachments/assets/8b1c528e-caaf-4cea-ae00-e074da3bc6f9" />

Agent Activity shows the autonomous decision-making process.

For every transaction, SecureRev can display:

- AI decision
- Decision reasoning
- Recovery score
- Security risk score
- Transaction ID
- Recovery result
- Amount recovered or prevented

Example:

```text
RETRY_PAYMENT

Temporary network timeout detected.
Customer has a strong successful-payment history.
No significant security anomalies detected.

Recovery Score: 80
Risk Score: 10

Result: ₹3,500 Recovered
