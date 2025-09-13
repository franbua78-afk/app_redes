## Deployment Guide

### Prerequisites
- Docker and Docker Compose
- Cloud S3 bucket (or keep MinIO)
- OAuth app credentials for Google (YouTube), TikTok, and Meta (Instagram)

### Environment
1. Copy `.env.example` to `.env` and set real values.
2. Set `DATABASE_URL` for production Postgres and `AWS_*` for real S3.
3. Set OAuth redirect URIs to `https://YOUR_API_DOMAIN/auth/google/callback` etc.

### Start
```bash
docker compose up -d --build
```

### Migrations
This starter uses SQLAlchemy create_all at startup. For production, add Alembic migrations.

### Workers
- `worker`: Celery worker (generate, upload, cleanup)
- `beat`: Celery beat (scheduler dispatch, cleanup)

### Domains and TLS
Put Nginx/Traefik in front, route `/` to frontend and `/api` to backend.

### Observability
- API health: GET `/health`
- Metrics: GET `/system/metrics`

