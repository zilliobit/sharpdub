from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.sessions import SessionMiddleware
from db.deps import get_db
from sqlalchemy import text
from db.redis import redis_client
import logging
from core.config import settings

from api import api_router
from apps.auth.routes_google import router as google_router

# Initialize the global logging configuration using dictConfig
logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger(__name__)

is_prod = settings.APP_ENV.lower() == "prod"

app = FastAPI(
    title=settings.APP_NAME,
    docs_url=None if is_prod else "/docs",
    redoc_url=None if is_prod else "/redoc",
    openapi_url=None if is_prod else "/openapi.json",
)
#this is for google oAuth2
app.add_middleware(
    SessionMiddleware, 
    secret_key=settings.SECRET_KEY  # Uses the key from your .env
) 

app.include_router(api_router, prefix="/api")
app.include_router(google_router)



@app.get("/", tags=["System"])
def root():
    return {"message": "API is running"}

@app.get("/db-connection-check", tags=["System"])
async def db_connection_check(db: AsyncSession = Depends(get_db)):
    """
    Database Connection Check.
    Tests the database connectivity by executing a simple 'SELECT version()' query.
    """
    try:
        await db.execute(text("SELECT version();"))
        logger.info("Database connection is healthy.")
        return {"status": "success", "database": "online"}
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Database connection failed"
        )

@app.get("/redis-connection-check", tags=["System"])
async def redis_connection_check():
    """
    Redis Connection Check.
    Tests the redis connectivity by executing a ping.
    """
    try:
        await redis_client.ping()
        logger.info("Redis connection is healthy.")
        return {"status": "success", "redis": "online"}
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail="Redis connection failed"
        )
    

