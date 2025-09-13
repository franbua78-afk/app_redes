from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "development"
    SECRET_KEY: str = "change_me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    BACKEND_CORS_ORIGINS: str = "http://localhost:8080"
    BACKEND_URL: str = "http://localhost:8000"
    FRONTEND_URL: str = "http://localhost:8080"

    DATABASE_URL: str = "postgresql+psycopg2://app:app@postgres:5432/app"
    REDIS_URL: str = "redis://redis:6379/0"

    S3_BUCKET: str = "media"
    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None
    AWS_S3_ENDPOINT_URL: str | None = None
    AWS_REGION: str = "us-east-1"

    GOOGLE_CLIENT_ID: str | None = None
    GOOGLE_CLIENT_SECRET: str | None = None
    GOOGLE_REDIRECT_URI: str | None = None

    TIKTOK_CLIENT_ID: str | None = None
    TIKTOK_CLIENT_SECRET: str | None = None
    TIKTOK_REDIRECT_URI: str | None = None

    META_APP_ID: str | None = None
    META_APP_SECRET: str | None = None
    META_REDIRECT_URI: str | None = None

    OPENAI_API_KEY: str | None = None
    ELEVENLABS_API_KEY: str | None = None
    STABILITY_API_KEY: str | None = None

    FFMPEG_BINARY: str = "ffmpeg"

    class Config:
        env_file = ".env"


settings = Settings()

