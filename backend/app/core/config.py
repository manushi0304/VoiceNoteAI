from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # =========================
    # App
    # =========================
    APP_NAME: str = "VoiceNote AI"
    ENV: str = "development"

    # =========================
    # Security
    # =========================
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # =========================
    # Database
    # =========================
    DATABASE_URL: str

    # =========================
    # Celery / Redis
    # =========================
    REDIS_URL: str | None = None

    # =========================
    # Email (SMTP) — reminders
    # =========================
    SMTP_HOST: str | None = None
    SMTP_PORT: int = 587
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    SMTP_FROM: str | None = None
    SMTP_USE_TLS: bool = True
    SMTP_USE_SSL: bool = False

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
