import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
from translator.translate import translate_en_to_tr
from constants import MODEL_ID
from agent.spoonacular_api import get_recipes_from_api, get_recipe_instructions
from agent import spoonacular_api


load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def get_recipe_list(ingredients: list[str], preference: str) -> str:
    prompt = f"""
You have these ingredients: {', '.join(ingredients)}.
You want a {preference.lower()} dish.
List ONLY the names of 3 meal suggestions I can make with them.
No explanations, no details. One per line, numbered.
""".strip()

    try:
        logging.info("Yemek listesi isteniyor (LLM)...")
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": "You are a helpful recipe suggester."},
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
        logging.error(f"Tarif listesi alınamadı (LLM): {e}")
        return ""

def ask_user_selection(options: list[str]) -> int:
    while True:
        selection = input("\nHangi tarifi detaylı istersiniz? (1 / 2 / 3): ").strip()
        if selection in {"1", "2", "3"}:
            return int(selection) - 1
        print("️ Lütfen sadece 1, 2 veya 3 girin.")

def get_recipe_instruction(recipe_name: str) -> str:
    prompt = f"""
Give step-by-step instructions for how to cook '{recipe_name}'.
Don't repeat the title. Use numbered steps. Be clear and concise.
Include approximate amounts or cooking times where possible.
""".strip()

    try:
        logging.info(f"'{recipe_name}' tarifi detaylı isteniyor (LLM)...")
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": "You are a professional chef."},
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
        logging.error(f"Tarif alınamadı (LLM): {e}")
        return ""

def run_agent_interactive(ingredients: list[str], preference: str) -> str:
    try:
        # Öncelik Spoonacular API
        recipes = get_recipes_from_api(ingredients, preference, number=3)
        if not recipes:
            raise ValueError("Boş liste")

        print("\n🍽️ Spoonacular'dan önerilen tarifler:")
        for i, r in enumerate(recipes, 1):
            print(f"{i}. {r['title']}")

        selected_index = ask_user_selection(recipes)
        selected_recipe = recipes[selected_index]

        detail_en = get_recipe_instructions(selected_recipe['id'])
        detail_tr = translate_en_to_tr(detail_en)

        return f"\n📝 **{selected_recipe['title']}** için adım adım tarif:\n\n{detail_tr}"

    except Exception as e:
        logging.warning(f"Spoonacular başarısız oldu, LLM'e geçiliyor: {e}")

        result_en = get_recipe_list(ingredients, preference)
        if not result_en:
            return "Hem Spoonacular hem LLM başarısız oldu. Daha sonra tekrar deneyin."

        print("\n🍽️ Sizin için önerilen tarifler (EN):\n" + result_en)
        result_tr = translate_en_to_tr(result_en)
        print("\n🍽️ Türkçe Çeviri:\n" + result_tr)

        recipe_lines = result_en.splitlines()
        selected_index = ask_user_selection(recipe_lines)

        try:
            selected_recipe = recipe_lines[selected_index].split(". ", 1)[1].strip()
        except:
            return "Tarif adı çözümlenemedi."

        detail_en = get_recipe_instruction(selected_recipe)
        detail_tr = translate_en_to_tr(detail_en)

        return f"\n📝 **{selected_recipe}** için adım adım tarif:\n\n{detail_tr}"
