"""
Yardımcı fonksiyonlar: kullanıcı girdisi temizleme, normalize etme vb.
"""

import re

def clean_ingredient_input(raw_input: str) -> list[str]:
    """
    Kullanıcının yazdığı malzeme metnini temiz listeye çevirir.
    Örn: " patates , yumurta , süt " → ["patates", "yumurta", "süt"]
    """
    return [i.strip().lower() for i in raw_input.split(",") if i.strip()]

def normalize_preference(preference_tr: str) -> str:
    """
    Türkçe tat tercihini normalize eder (tatlı / tuzlu → sweet / savory).
    """
    sweet_words = ["tatlı", "şekerli", "dessert"]
    savory_words = ["tuzlu", "yemek", "ana yemek", "acı", "tuz"]

    pref = preference_tr.strip().lower()

    if pref in sweet_words:
        return "sweet"
    elif pref in savory_words:
        return "savory"
    else:
        return "any"
