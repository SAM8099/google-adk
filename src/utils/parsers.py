import json

def format_agent_response(response):
    """Extracts text from agent response parts"""
    if response and hasattr(response, "content") and hasattr(response.content, "parts"):
        return " ".join(part.text for part in response.content.parts)
    return ""

def parse_json(text):
    """Attempts to parse a string as JSON, returning None if it fails."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None