"""
OpenRouter + OpenAI SDK 1.x ile çalışan Türkçe ↔ İngilizce çeviri modülü
"""

import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

MODEL = "deepseek/deepseek-r1-0528:free"


def call_openrouter(prompt: str) -> str:
    try:
        logging.info("Çeviri için OpenRouter çağrısı yapılıyor...")
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful translator."},
                {"role": "user", "content": prompt}
            ],
            extra_headers={
                "HTTP-Referer": "https://github.com/ozgurberkeakyol/recipe_agent",
                "X-Title": "recipe_agent"
            },
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"OpenRouter çeviri hatası: {e}")
        return "️ Çeviri sırasında bir hata oluştu."


def translate_tr_to_en(text: str) -> str:
    logging.info("Türkçeden İngilizceye çeviri başlatılıyor.")
    prompt = f"Sadece şu metni Türkçeden İngilizceye çevir, açıklama veya not E-KLE-ME:\n\n{text}"
    return call_openrouter(prompt)


def translate_en_to_tr(text: str) -> str:
    logging.info("İngilizceden Türkçeye çeviri başlatılıyor.")
    prompt = f"Sadece şu metni İngilizceden Türkçeye çevir, açıklama veya not E-KLE-ME:\n\n{text}"
    return call_openrouter(prompt)
