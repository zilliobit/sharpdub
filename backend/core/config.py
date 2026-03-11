#from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import os
from urllib.parse import quote_plus

# Load env ONCE
#load_dotenv()

class Settings(BaseSettings):
    APP_NAME:str
    APP_ENV:str 

    # Database & Security
    DB_CONNECTION: str
    DB_HOST: str
    DB_PORT: int
    DB_DATABASE: str
    DB_USERNAME: str
    DB_PASSWORD: str
   
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    

    SECRET_KEY: str

    # Google OAuth 
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    
    # Email Config (Matches your .env exactly)
    MAIL_HOST: str
    MAIL_PORT: int
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM_ADDRESS: str
    MAIL_FROM_NAME: str

    # DATABASE_URL is usually handled as a property or constant
    @property
    def DATABASE_URL(self) -> str:
        return f"{self.DB_CONNECTION}://{self.DB_USERNAME}:{quote_plus(self.DB_PASSWORD)}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"
        
    # Logging is usually handled as a property or constant
    @property
    def LOG_CONFIG(self) -> dict:
        if not os.path.exists("logs"):
            os.makedirs("logs")
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                    "stream": "ext://sys.stdout",
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "formatter": "standard",
                    "filename": "logs/app.log",
                    "maxBytes": 5242880,
                    "backupCount": 3,
                },
            },
            "root": {"level": "INFO", "handlers": ["console", "file"]},
        }

    class Config:
        env_file = ".env"
        extra = "ignore" # Ignores extra env vars not defined here

settings = Settings()
