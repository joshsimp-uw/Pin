import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def generate_response(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text
