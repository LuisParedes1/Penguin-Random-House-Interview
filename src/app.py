# app.py
"""
Set up for the app class
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import analysis

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis.router)
