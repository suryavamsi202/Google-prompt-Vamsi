from google import genai
from google.genai import types
from dotenv import load_dotenv
import os, json, re

# Explicitly load .env from the backend folder
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def build_prompt(input_type, raw_content, entities=None, context="general"):
    if entities is None:
        entities = []
    return f"""You are a Universal AI Bridge that converts messy real-world inputs into structured life-saving actions.

Input Type: {input_type}
Context: {context}
Entities: {entities}
Raw Input:
{raw_content}

Respond ONLY in this exact JSON (no markdown, no backticks):
{{
  "intent": "...",
  "urgency": "LOW|MEDIUM|HIGH|CRITICAL",
  "summary": "...",
  "category": "medical|traffic|weather|news|voice|general",
  "structured_data": {{}},
  "actions": ["action1", "action2"],
  "next_steps": ["step1", "step2"],
  "improved_prompt": "...",
  "confidence": 0.0
}}"""

def get_dynamic_client():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path=env_path, override=True)
    return genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def process_with_gemini(structured_input: dict) -> dict:
    client = get_dynamic_client()
    prompt = build_prompt(
        structured_input.get("input_type", "text"),
        structured_input.get("raw_content", ""),
        structured_input.get("entities", []),
        structured_input.get("context", "general")
    )
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        text = response.text.strip()
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception as e:
        print(f"Gemini error: {e}")
    return {"intent": "Unknown (API Key Expired/Missing)", "urgency": "LOW", "summary": "Could not process - Server key is stale or deleted.", "category": "general", "actions": [], "next_steps": [], "improved_prompt": "", "confidence": 0.0}

def process_image_with_gemini(image_bytes: bytes, mime_type: str = "image/jpeg") -> dict:
    client = get_dynamic_client()
    try:
        prompt = """Analyze this image as a Universal AI Bridge.
Respond ONLY in this exact JSON (no markdown):
{"intent":"...","urgency":"LOW|MEDIUM|HIGH|CRITICAL","summary":"...","category":"medical|traffic|weather|news|general","structured_data":{},"actions":["..."],"next_steps":["..."],"improved_prompt":"...","confidence":0.0}"""
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                prompt
            ]
        )
        text = response.text.strip()
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception as e:
        return {"summary": str(e), "urgency": "LOW", "actions": [], "intent": "Failed", "next_steps": [], "improved_prompt": "", "confidence": 0.0}
