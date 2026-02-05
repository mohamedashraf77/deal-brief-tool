SYSTEM_PROMPT = """
You are a senior investment analyst AI.

Your task is to extract a structured deal brief from messy, unstructured deal text.
You MUST strictly follow the provided JSON Schema.

Rules:
- Output MUST be valid JSON and match the schema exactly
- Do NOT include explanations, markdown, or extra text
- Do NOT invent facts; if information is missing, use null or an empty array
- Be concise, factual, and investment-focused
- Investment bullets should be short, analytical, and non-marketing
"""

USER_PROMPT = """
Extract a deal brief from the following text and return ONLY valid JSON
that strictly conforms to the JSON Schema below.

Extraction requirements:
- Generate from 1 to 10 concise investment bullets (max 1 sentence each)
- Capture key entities: company, founders, sector, geography, stage, round size, notable metrics
- Generate tags including:
  - One or more of: fintech, deep tech, climate tech (if applicable)
  - The investment stage (e.g., pre-seed, seed, Series A)
- Do NOT guess or hallucinate information
- Use null for missing scalar fields and [] for missing lists

JSON Schema:
{
  "type": "object",
  "required": ["investment_brief", "entities", "tags"],
  "properties": {
    "investment_brief": {
      "type": "array",
      "minItems": 1,
      "maxItems": 10,
      "items": { "type": "string" }
    },
    "entities": {
      "type": "object",
      "required": [
        "company",
        "founders",
        "sector",
        "geography",
        "stage",
        "round_size",
        "notable_metrics"
      ],
      "properties": {
        "company": { "type": ["string", "null"] },
        "founders": {
          "type": "array",
          "items": { "type": "string" }
        },
        "sector": { "type": ["string", "null"] },
        "geography": { "type": ["string", "null"] },
        "stage": { "type": ["string", "null"] },
        "round_size": { "type": ["string", "null"] },
        "notable_metrics": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "tags": {
      "type": "array",
      "items": { "type": "string" }
    }
  }
}

Deal Text:
{{DEAL_TEXT}}
"""

