"""
Spoonacular API ile tarif arama ve detay alma modülü.
"""

import os
import logging
import requests
from dotenv import load_dotenv

# Yükle ve log yapılandır
load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

API_KEY = os.getenv("SPOONACULAR_API_KEY")
BASE_URL_SEARCH = "https://api.spoonacular.com/recipes/complexSearch"
BASE_URL_INFO = "https://api.spoonacular.com/recipes/{id}/analyzedInstructions"


def get_recipes_from_api(ingredients: list[str], preference: str = "any", number: int = 3) -> list[dict]:
    if not API_KEY:
        logging.error("SPOONACULAR_API_KEY not found in environment variables.")
        raise EnvironmentError("SPOONACULAR_API_KEY not found in environment variables.")

    params = {
        "apiKey": API_KEY,
        "includeIngredients": ",".join(ingredients),
        "number": number,
        "instructionsRequired": True,
        "addRecipeInformation": True,
    }

    if preference.lower() == "sweet":
        params["query"] = "dessert"
    elif preference.lower() == "savory":
        params["query"] = "main course"

    try:
        logging.info("Spoonacular API üzerinden tarifler aranıyor...")
        response = requests.get(BASE_URL_SEARCH, params=params)
        response.raise_for_status()
        data = response.json()

        recipes = []
        for item in data.get("results", []):
            recipes.append({
                "id": item.get("id"),
                "title": item.get("title"),
                "url": item.get("sourceUrl", "No link available"),
            })

        if not recipes:
            logging.warning("API'den tarif bulunamadı.")
        else:
            logging.info(f"{len(recipes)} tarif bulundu.")

        return recipes

    except requests.exceptions.RequestException as e:
        logging.error(f"Spoonacular API hatası: {e}")
        return []


def get_recipe_instructions(recipe_id: int) -> str:
    url = BASE_URL_INFO.format(id=recipe_id)
    params = {"apiKey": API_KEY}

    try:
        logging.info(f"Tarif detayları alınıyor (ID: {recipe_id})...")
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if not data:
            logging.warning("Tarif için detay adım bilgisi boş döndü.")
            return "Bu tarif için adım bilgisi mevcut değil."

        steps = data[0].get("steps", [])
        if not steps:
            logging.warning("Tarif için adım bilgisi bulunamadı.")
            return "Adım bilgisi bulunamadı."

        return "\n".join([f"{step['number']}. {step['step']}" for step in steps])

    except requests.exceptions.RequestException as e:
        logging.error(f"Talimat API hatası: {e}")
        return "Tarif adımları alınırken bir hata oluştu."
