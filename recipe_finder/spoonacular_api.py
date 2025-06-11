"""
Spoonacular API ile tarif arama modülü.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SPOONACULAR_API_KEY")
BASE_URL = "https://api.spoonacular.com/recipes/complexSearch"

def get_recipes_from_api(ingredients: list[str], preference: str = "any", number: int = 3) -> list[dict]:
    """
    Spoonacular API'den tarifleri çeker.
    :param ingredients: ['potato', 'egg']
    :param preference: 'sweet' or 'savory'
    :param number: Kaç tarif getirilsin?
    :return: Liste: [{'title': ..., 'url': ...}, ...]
    """
    if not API_KEY:
        raise EnvironmentError("SPOONACULAR_API_KEY not found in environment variables.")

    # Parametreleri hazırla
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

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code} - {response.text}")

    data = response.json()

    recipes = []
    for item in data.get("results", []):
        recipes.append({
            "title": item.get("title"),
            "url": item.get("sourceUrl", "No link available"),
        })

    return recipes
