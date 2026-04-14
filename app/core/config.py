from pathlib import Path
import os

class Settings:
    app_name: str = os.getenv("APP_NAME", "Sentinela Operacional API")
    secret_key: str = os.getenv("SECRET_KEY", "troque-esta-chave")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "720"))
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./sentinela_local.db")
    cors_origins: list[str] = [i.strip() for i in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",") if i.strip()]
    base_dir = Path(__file__).resolve().parents[2]
    uploads_dir = base_dir / "uploads"
    fotos_dir = uploads_dir / "fotos"
    assinaturas_dir = uploads_dir / "assinaturas"

settings = Settings()
settings.fotos_dir.mkdir(parents=True, exist_ok=True)
settings.assinaturas_dir.mkdir(parents=True, exist_ok=True)
