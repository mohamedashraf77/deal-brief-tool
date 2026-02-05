import json
from utils import count_tokens, clean_text, hash_text
from llm import llm
from schema import validate_deal_json
from storage import DealDatabase

MAX_TOKENS = 3000


def run_pipeline(raw_text: str):
    db = DealDatabase()
    llm_instance = llm()

    tokens = count_tokens(raw_text)
    if tokens > MAX_TOKENS:
        raise ValueError("Input too large")

    cleaned = clean_text(raw_text)
    text_hash = hash_text(cleaned)

    try:
        llm_output = llm_instance.extract_with_llm(cleaned)
        data = json.loads(llm_output)
        validate_deal_json(data)

        db.save_deal(text_hash, raw_text, data, "success")
        return data

    except json.JSONDecodeError:
        db.save_deal(text_hash, raw_text, None, "error", "Invalid JSON")
        raise

    except Exception as e:
        db.save_deal(text_hash, raw_text, None, "error", str(e))
        raise
