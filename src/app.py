# app.py
"""
Set up for the app class
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import analysis
import pandas as pd
from dotenv import load_dotenv
import os

def load_data() -> pd.DataFrame:
    df = pd.read_csv(os.getenv("DATA_PATH"), 
                     dtype={"country": "string","value": "float"}) 
    df["fecha"] = pd.to_datetime(df["fecha"], format="%d/%m/%Y", errors="coerce")
    return df


load_dotenv()
DATA: pd.DataFrame = load_data()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis.router)