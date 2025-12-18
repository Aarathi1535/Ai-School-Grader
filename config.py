# config.py
import os

AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_KEY      = os.getenv("AZURE_KEY")

GROQ_API_KEY   = os.getenv("GROQ_API_KEY")

GROQ_MODEL_EXTRACTION = "llama-3.3-70b-versatile"
GROQ_MODEL_GRADING    = "llama-3.1-8b-instant"



