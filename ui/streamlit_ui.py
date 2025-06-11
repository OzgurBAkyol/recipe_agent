"""
Web arayüzü: Kullanıcıdan malzeme ve tercih alır, AI ile tarif önerir.
"""

import streamlit as st

from translator.translate import translate_tr_to_en
from utils.helpers import clean_ingredient_input, normalize_preference
from agent.recipe_agent import run_agent

def run_ui():
    st.set_page_config(page_title="🍽️ AI Yemek Asistanı")
    st.title("🤖 Akıllı Yemek Tarifi Asistanı")
    st.write("📋 Elinizdeki malzemeleri girin, nasıl bir yemek istediğinizi seçin, biz sizin yerinize tarifi bulalım!")

    with st.form("input_form"):
        raw_ingredients = st.text_input("🧾 Malzemeleri girin (örn: patates, yumurta, süt)")
        preference = st.selectbox("🎯 Tat tercihiniz nedir?", ["Tuzlu", "Tatlı", "Farketmez"])

        submitted = st.form_submit_button("Tarif öner!")

    if submitted:
        if not raw_ingredients:
            st.warning("Lütfen en az bir malzeme girin.")
            return

        # Malzemeleri temizle
        ingredients_tr = clean_ingredient_input(raw_ingredients)
        ingredients_en = translate_tr_to_en(", ".join(ingredients_tr)).split(",")
        ingredients_en = [i.strip().lower() for i in ingredients_en]

        # Tat tercihini normalize et ve çevir
        pref_normalized = normalize_preference(preference)
        pref_en = translate_tr_to_en(pref_normalized)

        # Agent'ı çalıştır
        with st.spinner("🧠 AI tarif öneriyor..."):
            result = run_agent(ingredients_en, pref_en)

        # Sonuç
        st.success("🎉 Tarifleriniz hazır!")
        st.markdown("### 🍽️ Önerilen Tarifler:")
        st.markdown(result)
