# SecureRev — Autonomous Secure Revenue Recovery Agent
# Dashboard   <img width="1887" height="876" alt="image" src="https://github.com/user-attachments/assets/cd274662-73e1-48d0-bb4f-ad67116c9c57" />
# Transactions  <img width="1860" height="874" alt="image" src="https://github.com/user-attachments/assets/32405555-14e6-463d-9ad6-ad4dad3d936a" />
# Agent Activity  <img width="1863" height="876" alt="image" src="https://github.com/user-attachments/assets/8b1c528e-caaf-4cea-ae00-e074da3bc6f9" />
# Test Payment / Simulation  <img width="1896" height="873" alt="image" src="https://github.com/user-attachments/assets/f289e882-b9f8-4713-a6e1-e921ab58a341" />
# Mock Razorpay 

<img width="941" height="436" alt="image" src="https://github.com/user-attachments/assets/a2ac9871-b60c-4909-a32a-854eab85ae5e" />
<img width="936" height="431" alt="image" src="https://github.com/user-attachments/assets/f2f81cb4-9ee5-4719-981e-06488cf3bd3c" />
<img width="1677" height="994" alt="image" src="https://github.com/user-attachments/assets/ea1563d1-2c6a-4057-a799-3fd170b47a18" />
<img width="1558" height="832" alt="image" src="https://github.com/user-attachments/assets/a3ea8c87-8bd7-435f-a1d4-6e0805bbf760" />
<img width="1636" height="892" alt="image" src="https://github.com/user-attachments/assets/2b7a5c66-cdad-45a3-aa69-5350d35a5ea2" />

SecureRev is a B2B fintech platform designed to recover legitimate failed payments while preventing suspicious or high-risk transactions from being automatically recovered. Built for merchants using Razorpay, SecureRev combines Revenue Recovery Intelligence with Payment Security Intelligence through a deterministic Policy Engine and an AI Agent.

> **Disclaimer:** SecureRev is a hackathon prototype and does not represent a production integration with Razorpay. All Razorpay interactions happen in Test Mode or are simulated.

## Problem
Merchants lose significant revenue to legitimate payment failures (e.g., temporary network timeouts, insufficient funds). However, blindly retrying failed payments increases the risk of processing fraudulent transactions, violating rate limits, or incurring penalty fees.

## Solution
SecureRev solves this by introducing dual-track intelligence:
1. **Security Intelligence Engine:** Determines if a transaction is safe to recover (analyzing velocity, device anomalies, payment switching, etc.).
2. **Recovery Intelligence Engine:** Evaluates the likelihood of a successful recovery and recommends the optimal strategy (Retry, Payment Link, etc.).
3. **Policy Engine & AI Agent:** The AI Agent recommends an action based on context, which is then strictly validated by a deterministic Policy Engine before execution.

## Architecture & Tech Stack
- **Frontend:** Next.js, React, TypeScript, Tailwind CSS, Recharts
- **Backend:** Python, FastAPI, SQLAlchemy, Pydantic
- **Database:** PostgreSQL
- **Infrastructure:** Docker, Docker Compose
- **Integrations:** Razorpay API (Test Mode), LLM API (for transaction interpretation)

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Razorpay Test Account credentials
- LLM API Key (e.g., Gemini/OpenAI)

### Setup Instructions
1. Clone the repository (if applicable) or navigate to the project directory.
2. Copy `.env.example` to `.env` and fill in your credentials.
3. Start the application:
   ```bash
   docker compose up --build
   ```
4. Access the application:
   - Frontend: `http://localhost:3000`
   - Backend API Docs: `http://localhost:8000/docs`
   - Backend Health Check: `http://localhost:8000/api/v1/health`

## Hackathon Positioning
SecureRev belongs to the **AI Revenue Recovery** track. It is a B2B application focusing on merchant revenue optimization and security, featuring explainable AI and strict deterministic bounding to prevent unauthorized financial actions.
