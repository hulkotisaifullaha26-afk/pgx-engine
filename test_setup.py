import pdfplumber
import anthropic
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("ANTHROPIC_API_KEY")

if key:
    print("Setup complete. API key loaded.")
else:
    print("API key not found. Check your .env file.")