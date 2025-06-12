"""
Terminal tabanlı kullanıcı arayüzü.
Kullanıcıdan Türkçe giriş alır, agent çalıştırır, Türkçe sonuç verir.
"""

import logging
from translator.translate import translate_tr_to_en
from utils.helpers import clean_ingredient_input, normalize_preference
from agent.recipe_agent import run_agent_interactive  # Güncel fonksiyon
from agent import spoonacular_api


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def run_cli():
    print("🧠 Hoş geldiniz! Elinizdeki malzemeleri ve isteğinizi girin.\n")

    try:
        raw_ingredients = input("Malzemeleri girin (örn: patates, yumurta, süt): ").strip()
        preference = input("Tat tercihiniz nedir? (tatlı / tuzlu): ").strip().lower()

        if not raw_ingredients:
            print("⚠️ Malzeme listesi boş olamaz.")
            return

        if preference not in {"tatlı", "tuzlu"}:
            print("⚠️ Tat tercihiniz sadece 'tatlı' veya 'tuzlu' olabilir.")
            return

        # Temizle ve çevir
        ingredients_list_tr = clean_ingredient_input(raw_ingredients)
        ingredients_text_en = translate_tr_to_en(", ".join(ingredients_list_tr))
        ingredients_list_en = [i.strip().lower() for i in ingredients_text_en.split(",")]

        preference_clean = normalize_preference(preference)
        preference_en = translate_tr_to_en(preference_clean)

        logging.info("Tarif önerisi başlatılıyor...")
        print("\n🍳 Tarifler aranıyor...")
        result = run_agent_interactive(ingredients_list_en, preference_en)

        print(result)

    except Exception as e:
        logging.error(f"Bir hata oluştu: {e}")
        print("️ Beklenmeyen bir hata oluştu. Lütfen tekrar deneyin.")
