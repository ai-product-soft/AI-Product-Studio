from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    OLLAMA_URL: str = "http://ollama:11434"
    OLLAMA_MODEL: str = "mistral:7b-instruct-v0.2-q4_K_M"
    EMBED_MODEL: str = "nomic-embed-text"
    STRIPE_API_KEY: str = ""
    DELIVERY_SECRET: str = "change-me-in-production"
    ENCRYPTION_KEY: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
