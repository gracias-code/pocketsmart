from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import get_settings
from app.database import init_db
from app.routes import auth,pages,planners

@asynccontextmanager
async def lifespan(app):
    init_db()
    yield

s=get_settings()
app=FastAPI(title=s.app_name,version="1.0.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=[x.strip() for x in s.cors_origins.split(",")],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.mount("/static",StaticFiles(directory="app/static"),name="static")
app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(planners.router)
