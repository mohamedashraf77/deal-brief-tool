from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pipeline import run_pipeline
from storage import DealDatabase
from utils import count_tokens
import os
import dotenv

dotenv.load_dotenv()

MAX_TOKENS = int(os.getenv("MAX_TOKENS", 3000))

app = FastAPI(title="Deal Brief API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


db = DealDatabase()

@app.get("/alive")
def alive():
    return {"status": "ok"}

@app.get("/deals")
def list_deals():
    return db.get_latest_deals()

@app.get("/deals/{deal_id}")
def get_deal(deal_id: int):
    print(f"Fetching deal with ID: {db.get_deal_by_id(deal_id)}")
    return db.get_deal_by_id(deal_id)

@app.post("/deal")
def create_deal(payload: dict):
    if "text" not in payload:
        raise HTTPException(400, "Missing text")
    
    text = payload["text"]
    tokens = count_tokens(text)
    if tokens > MAX_TOKENS:
        db.save_deal("N/A", text, None, "error", f"Too many tokens ({tokens})")
        raise HTTPException(400, f"Input too large ({tokens} tokens, max {MAX_TOKENS})")
    
    try:
        result = run_pipeline(text)
        return result
    except Exception as e:
        raise HTTPException(400, str(e))
