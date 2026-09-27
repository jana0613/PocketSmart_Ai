import json
from typing import Optional
from google import genai
from google.genai import types
from ..config import get_settings

class GeminiService:
    def __init__(self):
        settings = get_settings()
        self.enabled = bool(settings.gemini_api_key)
        self.model = settings.gemini_model
        self.client = genai.Client(api_key=settings.gemini_api_key) if self.enabled else None

    def generate(self, prompt: str, image_bytes: Optional[bytes] = None, mime_type: Optional[str] = None) -> Optional[dict]:
        if not self.enabled:
            return None
        contents = [prompt]
        if image_bytes and mime_type:
            contents.insert(0, types.Part.from_bytes(data=image_bytes, mime_type=mime_type))
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.4,
                    max_output_tokens=4096,
                ),
            )
            text = response.text.strip()
            return json.loads(text)
        except Exception:
            return None
