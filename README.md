# Bharosa AI
AI trust platform built with Django: LLM gateway with PII masking, AI red-team tester, DPDP readiness check, and Kagaz Samjhao document explainer.

## Run (Windows PowerShell / VS Code terminal)
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    python manage.py makemigrations core
    python manage.py migrate
    python manage.py test
    python manage.py runserver
Open http://127.0.0.1:8000

Runs in demo mode by default. For real AI answers set `ANTHROPIC_API_KEY` (see .env.example):
    $env:ANTHROPIC_API_KEY="your-key"

## Extras
- Docker: `docker build -t bharosa-ai .` then `docker run -p 8000:8000 bharosa-ai`
- CI: GitHub Actions runs tests on every push (`.github/workflows/ci.yml`)
- Health check: `/health/` | API: `POST /api/gateway/` returns masked prompt, PII types and reply
- Shortcuts: Alt+H / G / R / D / K | Theme toggle (light/dark) in the header
