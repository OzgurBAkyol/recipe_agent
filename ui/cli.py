"""
Terminal tabanlı kullanıcı arayüzü.
Kullanıcıdan Türkçe giriş alır, agent çalıştırır, Türkçe sonuç verir.
"""

from translator.translate import translate_tr_to_en
from utils.helpers import clean_ingredient_input, normalize_preference
from agent.recipe_agent import run_agent_interactive  # Güncel fonksiyon

def run_cli():
    print("🧠 Hoş geldiniz! Elinizdeki malzemeleri ve isteğinizi girin.\n")

    # Kullanıcıdan giriş al
    raw_ingredients = input("Malzemeleri girin (örn: patates, yumurta, süt): ")
    preference = input("Tat tercihiniz nedir? (tatlı / tuzlu): ")

    # Temizle ve İngilizce'ye çevir
    ingredients_list_tr = clean_ingredient_input(raw_ingredients)
    ingredients_text_en = translate_tr_to_en(", ".join(ingredients_list_tr))
    ingredients_list_en = [i.strip().lower() for i in ingredients_text_en.split(",")]

    # Tat tercihini normalize et (tatlı → sweet, tuzlu → savory)
    preference_clean = normalize_preference(preference)
    preference_en = translate_tr_to_en(preference_clean)

    # Agent'ı çalıştır
    print("\n🍳 Tarifler aranıyor...")
    result = run_agent_interactive(ingredients_list_en, preference_en)

    # Sonucu göster
    print(result)
