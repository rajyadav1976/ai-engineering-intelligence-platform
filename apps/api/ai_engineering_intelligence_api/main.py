from fastapi import FastAPI
from .routes.health import router as health_router

app=FastAPI(title="AI Engineering Intelligence API", 
            description="API for AI Engineering Intelligence", 
            version="1.0.0"
            )

app.include_router(health_router)