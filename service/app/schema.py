from jsonschema import validate

DEAL_SCHEMA = {
    "type": "object",
    "required": ["investment_brief", "entities", "tags"],
    "properties": {
        "investment_brief": {
            "type": ["array", "null"],
            "items": {"type": "string"},
            "minItems": 1,
            "maxItems": 10
        },
        "entities": {
            "type": "object",
            "required": [
                "company", "founders", "sector",
                "geography", "stage", "round_size",
                "notable_metrics"
            ],
            "properties": {
                "company": {"type": ["string", "null"]},
                "founders": {"type":["array", "null"], "items": {"type": "string"}},
                "sector": {"type": ["string", "null"]},
                "geography": {"type": ["string", "null"]},
                "stage": {"type": ["string", "null"]},
                "round_size": {"type": ["string", "null"]},
                "notable_metrics": {"type": ["array", "null"], "items": {"type": "string"}}
            }
        },
        "tags": {"type": ["array", "null"], "items": {"type": "string"}}
    }
}


def validate_deal_json(data: dict):
    validate(instance=data, schema=DEAL_SCHEMA)