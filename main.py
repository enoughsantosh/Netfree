from fastapi import FastAPI, HTTPException
import httpx
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware
import logging
import re
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Anime Search API is running!"}


