from fastapi import FastAPI, HTTPException
from pipeline import run_pipeline

app = FastAPI()


@app.post("/deal")
def create_deal(payload: dict):
    if "text" not in payload:
        raise HTTPException(400, "Missing text")

    try:
        return run_pipeline(payload["text"])
    except Exception as e:
        raise HTTPException(400, str(e))
