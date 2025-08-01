# FastAPI Backend Project

This is a production-ready Python backend project built with FastAPI, featuring authentication, authorization, metrics tracking, OTP integration, and email notifications.

## Features
- 🔐 JWT-based Authentication & Role-Based Access Control (RBAC)
- 📁 Modular Project Structure
- 📊 API Health & Metrics Tracking
- 📡 SMS & Email OTP Integration
- ✉️ Email Notifications
- 🔐 Middleware & Dependencies for security and logging

## Tech Stack
- FastAPI (web framework)
- SQLAlchemy (ORM)
- Alembic (migrations)
- PostgreSQL/MySQL (database)
- Pydantic (data validation)
- JWT (python-jose)
- Environment config (python-dotenv)
- Email (SMTP/SendGrid), SMS (Twilio)

## Setup
1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Configure environment variables**:
   Copy `.env.example` to `.env` and update the values.
3. **Run database migrations**:
   ```bash
   alembic upgrade head
   ```
4. **Start the server**:
   ```bash
   uvicorn src.main:app --reload
   ```

## Running Tests
```bash
pytest
```

## Docker Support
(Optional) Build and run with Docker:
```bash
docker build -t fastapi-backend .
docker run -p 8000:8000 fastapi-backend
```
