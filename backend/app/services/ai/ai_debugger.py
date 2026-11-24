import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.prompts.debugging_prompt import DEBUGGING_SYSTEM_PROMPT

BACKEND_DIR = Path(__file__).resolve().parents[3]
load_dotenv(BACKEND_DIR / ".env", override=True)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def analyze_with_ai(code: str, analysis: dict) -> dict:
    if not API_KEY:
        return {"status": "unavailable", "message": "Gemini API key is missing."}

    client = genai.Client(api_key=API_KEY)
    payload = json.dumps({
        "submitted_code": code,
        "static_analysis_results": analysis
    }, indent=2)

    for attempt in range(2):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=payload,
                config=types.GenerateContentConfig(
                    system_instruction=DEBUGGING_SYSTEM_PROMPT,
                    temperature=0.2,
                    max_output_tokens=1500
                )
            )

            if not response.text:
                return {"status": "unavailable", "message": "Gemini returned an empty response."}

            return {
                "status": "success",
                "provider": "Google Gemini",
                "model": MODEL,
                "explanation": response.text
            }

        except Exception as error:
            error_name = type(error).__name__

            if attempt == 0 and error_name in {
                "ServerError", "ServiceUnavailable", "TimeoutError"
            }:
                time.sleep(2)
                continue

            return {
                "status": "unavailable",
                "provider": "Google Gemini",
                "message": f"AI service temporarily unavailable ({error_name}).",
            }

    return {"status": "unavailable", "message": "AI service unavailable."}
