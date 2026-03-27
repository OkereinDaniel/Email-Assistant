from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    app_env: str = "development"
    secret_key: str

    # Supabase
    supabase_url: str
    supabase_service_role_key: str

    # Google OAuth / Gmail
    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str = "http://localhost:8000/auth/callback/google"

    # AI Providers
    anthropic_api_key: str
    openai_api_key: str

    # Integrations
    slack_bot_token: str = ""
    notion_api_key: str = ""

    # Redis (job queue)
    redis_url: str = "redis://localhost:6379"

    class Config:
        env_file = "../.env"


settings = Settings()
