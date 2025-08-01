from pydantic import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost/dbname"
    
    # JWT
    JWT_SECRET_KEY: str = "your-secret-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # Email
    EMAIL_HOST: str = "smtp.sendgrid.net"
    EMAIL_PORT: int = 587
    EMAIL_USERNAME: str = "apikey"
    EMAIL_PASSWORD: str = "your-sendgrid-api-key"
    EMAIL_FROM: str = "noreply@yourdomain.com"
    
    # SMS (Twilio)
    TWILIO_ACCOUNT_SID: str = "your-twilio-account-sid"
    TWILIO_AUTH_TOKEN: str = "your-twilio-auth-token"
    TWILIO_FROM_NUMBER: str = "+1234567890"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
