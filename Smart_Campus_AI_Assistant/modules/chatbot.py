import os
from dotenv import load_dotenv
load_dotenv()
def answer_question(question):
    key=os.getenv("GEMINI_API_KEY","").strip()
    if not key:
        return ("Gemini is not configured. Copy .env.example to .env and add GEMINI_API_KEY. Local modules work without it.","Local fallback; no AI API call.")
    try:
        from google import genai
        client=genai.Client(api_key=key)
        response=client.models.generate_content(model=os.getenv("GEMINI_MODEL","gemini-2.5-flash"),contents=question)
        return response.text or "Empty response.","Gemini API response."
    except Exception as e: return f"Gemini request failed: {e}","Check key, quota, model access and internet."
