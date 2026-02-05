from jsonschema import validate, ValidationError

DEAL_SCHEMA = {
    "type": "object",
    "required": ["investment_brief", "entities", "tags"],
    "properties": {
        "investment_brief": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 5,
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
                "company": {"type": "string"},
                "founders": {"type": "array", "items": {"type": "string"}},
                "sector": {"type": "string"},
                "geography": {"type": "string"},
                "stage": {"type": "string"},
                "round_size": {"type": "string"},
                "notable_metrics": {"type": "array", "items": {"type": "string"}}
            }
        },
        "tags": {"type": "array", "items": {"type": "string"}}
    }
}


def validate_deal_json(data: dict):
    validate(instance=data, schema=DEAL_SCHEMA)