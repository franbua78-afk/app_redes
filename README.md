## AI Shorts Studio

Production-ready web app to generate, schedule, and auto-upload short-form vertical videos (Shorts/Reels/TikToks).

### Stack
- Backend: FastAPI (Python 3.11), Celery, Redis, SQLAlchemy, PostgreSQL
- Frontend: React (Vite) + Tailwind CSS, served by Nginx
- Storage: S3-compatible (MinIO locally), boto3
- Video: MoviePy + FFmpeg, AI providers (OpenAI/ElevenLabs/Stability)
- OAuth: Google (YouTube), TikTok, Instagram (Meta)
- CI/CD: GitHub Actions

### Quick Start

1. Copy env
```bash
cp .env.example .env
```

2. Launch
```bash
docker compose up -d --build
```

3. Open UI
- Frontend: http://localhost:8080
- API docs: http://localhost:8000/docs

### Features
- Generate script → TTS → visuals → merge to 1080x1920 MP4
- Auto-thumbnail, S3 upload, temp cleanup
- OAuth2 for platforms with token refresh
- Immediate or scheduled posting via Celery
- Dashboard with real-time status, calendar, analytics

### Configuration Notes
- For S3 in local dev we use MinIO. Credentials are in `.env.example`.
- Provide AI keys (OpenAI/ElevenLabs/Stability) to enable full generation. Without them, the app falls back to simple text-slides with generated music muted.
- For YouTube uploads, set Google OAuth credentials and authorized redirect URI: `http://localhost:8000/auth/google/callback`.

### Development
- Backend hot-reload: edit code and restart container if necessary.
- Frontend uses a multi-stage Dockerfile to build and serve from Nginx.

### Deployment
- Set production `.env` values and remove MinIO if using AWS S3.
- Use the provided GitHub Actions workflow to build and push images.

# app_redes
automatizar redes
