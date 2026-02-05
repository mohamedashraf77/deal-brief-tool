import json
from utils import count_tokens, clean_text, hash_text
from llm import llm
from schema import validate_deal_json
from storage import init_db, save_deal

MAX_TOKENS = 3000


def run_pipeline(raw_text: str):
    conn = init_db()
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

        save_deal(conn, text_hash, raw_text, json.dumps(data), "success")
        return data

    except json.JSONDecodeError:
        save_deal(conn, text_hash, raw_text, None, "error", "Invalid JSON")
        raise

    except Exception as e:
        save_deal(conn, text_hash, raw_text, None, "error", str(e))
        raise
