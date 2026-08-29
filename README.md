# SecureRev — Autonomous Secure Revenue Recovery Agent

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
