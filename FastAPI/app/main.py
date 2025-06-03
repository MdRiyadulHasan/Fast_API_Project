# app/main.py
from fastapi import FastAPI
from app.api.v1.api import api_router

app = FastAPI(title="My FastAPI Project with Multiple Apps")

app.include_router(api_router, prefix="/api/v1")