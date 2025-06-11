"""
OpenRouter destekli tarif üretici. Kullanıcının verdiği malzeme ve tercihe göre önce yemek önerir,
ardından seçilen tarifin adım adım nasıl yapılacağını açıklar.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
from translator.translate import translate_en_to_tr

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

MODEL = "deepseek/deepseek-r1-0528:free"

def run_agent_interactive(ingredients: list[str], preference: str) -> str:
    """
    Önce yemek önerilerini listeler, sonra kullanıcıdan seçim alır ve tarifi detaylı anlatır.
    Çıktı Türkçe döner.
    """
    # 1. Tarif isimlerini al
    query = f"You have these ingredients: {', '.join(ingredients)}. You want a {preference.lower()} dish. List 3 meal suggestions I can make with them. Only list names."

    print(f"\n🔍 Agent Query (EN): {query}")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a professional recipe suggester."},
            {"role": "user", "content": query}
        ],
        extra_headers={
            "HTTP-Referer": "https://github.com/ozgurberkeakyol/recipe_agent",
            "X-Title": "recipe_agent"
        },
        temperature=0.3
    )

    result_en = response.choices[0].message.content.strip()
    print(f"\n🍽️ Sizin için önerilen tarifler (EN):\n{result_en}")

    # Türkçeye çevirip göster
    result_tr = translate_en_to_tr(result_en)
    print(f"\n🍽️ Türkçe Çeviri:\n{result_tr}")

    # 2. Kullanıcıdan seçim al
    selection = input("\nHangi tarifi detaylı istersiniz? (1 / 2 / 3): ").strip()
    if selection not in {"1", "2", "3"}:
        return "Geçersiz seçim yapıldı. Lütfen sadece 1, 2 veya 3 girin."

    # 3. Seçilen tarifin adını çöz
    try:
        selected_line = result_en.splitlines()[int(selection) - 1]
        selected_recipe_name = selected_line.split(". ", 1)[1].strip()
    except:
        return "Tarif adı çözümlenemedi."

    # 4. Tarif detayı isteme
    detail_prompt = f"How do I prepare '{selected_recipe_name}'? Give step-by-step cooking instructions. Don't repeat the title."

    detail_response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a professional chef."},
            {"role": "user", "content": detail_prompt}
        ],
        extra_headers={
            "HTTP-Referer": "https://github.com/ozgurberkeakyol/recipe_agent",
            "X-Title": "recipe_agent"
        },
        temperature=0.3
    )

    detail_en = detail_response.choices[0].message.content.strip()
    detail_tr = translate_en_to_tr(detail_en)

    return f"\n📝 **{selected_recipe_name}** için adım adım tarif:\n\n{detail_tr}"
