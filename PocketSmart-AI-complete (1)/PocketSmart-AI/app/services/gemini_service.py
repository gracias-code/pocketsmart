import json, re
from app.config import get_settings

def parse_json(text):
    text = re.sub(r"^```json\s*|^```\s*|\s*```$", "", text.strip())
    m = re.search(r"\{.*\}", text, re.S)
    return json.loads(m.group(0) if m else text)

def generate(prompt, image_bytes=None, mime_type=None):
    s = get_settings()
    if not s.gemini_api_key:
        return None
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=s.gemini_api_key)
        contents = [prompt]
        if image_bytes and mime_type:
            contents.insert(0, types.Part.from_bytes(data=image_bytes, mime_type=mime_type))
        response = client.models.generate_content(
            model=s.gemini_model,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.3,
                response_mime_type="application/json"
            )
        )
        return parse_json(response.text)
    except Exception:
        return None
