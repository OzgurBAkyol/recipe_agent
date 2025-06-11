"""
OpenRouter + OpenAI SDK 1.x ile çalışan Türkçe ↔ İngilizce çeviri modülü
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

MODEL = "deepseek/deepseek-r1-0528:free"

def call_openrouter(prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful translator."},
            {"role": "user", "content": prompt}
        ],
        extra_headers={
            "HTTP-Referer": "https://github.com/ozgurberkeakyol/recipe_agent",  # isteğe bağlı
            "X-Title": "recipe_agent"
        }
    )
    return response.choices[0].message.content.strip()

def translate_tr_to_en(text: str) -> str:
    prompt = f"Sadece şu metni Türkçeden İngilizceye çevir, açıklama veya not E-KLE-ME:\n\n{text}"
    return call_openrouter(prompt)

def translate_en_to_tr(text: str) -> str:
    prompt = f"Sadece şu metni İngilizceden Türkçeye çevir, açıklama veya not E-KLE-ME:\n\n{text}"
    return call_openrouter(prompt)

