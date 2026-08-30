<div align="center">

<img src="https://razorpay.com/assets/razorpay-glyph.svg" alt="Razorpay" width="70"/>

# SecureRev — Autonomous Secure Revenue Recovery Agent

**AI-Powered Revenue Recovery • Razorpay Test Mode • Bounded Autonomous Decisions**

![Next.js](https://img.shields.io/badge/Next.js-000000?logo=next.js&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?logo=tailwindcss&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

**Payment Platform:** Razorpay Test Mode / Controlled Simulation

</div>

---


SecureRev is a B2B fintech platform designed to help merchants recover legitimate failed payments while preventing unsafe or suspicious transactions from being automatically recovered.

The system combines **Revenue Recovery Intelligence, Payment Security Intelligence, an AI Decision Agent, and a deterministic Policy Engine** to create a bounded autonomous recovery workflow.

> **Disclaimer:** SecureRev is a hackathon prototype. It does not represent a production integration with Razorpay. Razorpay interactions are performed in Test Mode or through controlled simulations. No real customer money is processed by the prototype.
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

# Mock Razorpay

SecureRev also includes a controlled Razorpay-style simulation environment.

<img width="941" height="436" alt="Mock Razorpay 1" src="https://github.com/user-attachments/assets/a2ac9871-b60c-4909-a32a-854eab85ae5e" /> <img width="936" height="431" alt="Mock Razorpay 2" src="https://github.com/user-attachments/assets/f2f81cb4-9ee5-4719-981e-06488cf3bd3c" /> <img width="1677" height="994" alt="Mock Razorpay 3" src="https://github.com/user-attachments/assets/ea1563d1-2c6a-4057-a799-3fd170b47a18" /> <img width="1558" height="832" alt="Mock Razorpay 4" src="https://github.com/user-attachments/assets/a3ea8c87-8bd7-435f-a1d4-6e0805bbf760" /> <img width="1636" height="892" alt="Mock Razorpay 5" src="https://github.com/user-attachments/assets/2b7a5c66-cdad-45a3-aa69-5350d35a5ea2" />

The mock environment is used to demonstrate payment states and recovery scenarios safely.

No real customer payment is processed.

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

```
## Demo Flow

The following demo flow demonstrates the complete SecureRev revenue recovery lifecycle from detection to measurable recovery.

### Merchant Demo Walkthrough

```text
1. Open Dashboard
        ↓
2. Show Revenue at Risk
        ↓
3. Click "Run Demo Simulation"
        ↓
4. Generate Multiple Failed Transactions
        ↓
5. Open Transactions
        ↓
6. Show Different Failure Reasons
        ↓
7. Show LOW / MEDIUM / HIGH Risk Levels
        ↓
8. Open Agent Activity
        ↓
9. Show AI Reasoning
        ↓
10. Show Recovery Score
        ↓
11. Show Security Risk Score
        ↓
12. Show AI Decision
        ↓
13. Show Policy-Controlled Action
        ↓
14. Show Recovered Amount
        ↓
15. Show Escalated High-Risk Transaction
        ↓
16. Return to Dashboard
        ↓
17. Show Final Batch Recovery Metrics
```
## Project Structure

```text
securerev/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── policies/
│   │   ├── agents/
│   │   └── main.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── pages/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── generate_code.py
├── run_local_simulation.py
└── README.md
```
## SecureRev System Workflow

SecureRev follows an end-to-end autonomous revenue recovery workflow:

```text
Revenue Detection
        ↓
Failure Diagnosis
        ↓
Security Analysis
        ↓
Recovery Intelligence
        ↓
AI Decision
        ↓
Policy Validation
        ↓
Bounded Recovery
        ↓
Measured Revenue
        ↓
Audit Trail
