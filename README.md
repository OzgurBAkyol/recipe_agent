# 🤖 Recipe Agent — Akıllı Yemek Tarifi Asistanı

Elinizdeki malzemelere ve damak tadınıza göre size özel yemek tarifleri öneren bir AI destekli uygulama.  
Spoonacular API kullanarak gerçek tarifleri alır, gerekirse LLM (DeepSeek) ile öneri üretir ve sonuçları Türkçe olarak sunar.

## 🚀 Özellikler

-  OpenRouter destekli LLM (DeepSeek) ile tarif önerileri
-  Spoonacular API ile gerçek tarif ve pişirme adımları
-  Streamlit ile Web UI, Terminal üzerinden CLI desteği
-  Türkçe ↔ İngilizce çeviri entegrasyonu (LLM tabanlı)
-  Hata yönetimi, logging ve fallback mimarisi

---

## 📦 Kurulum

```bash
git clone https://github.com/ozgurberkeakyol/recipe_agent.git
cd recipe_agent
pip install -r requirements.txt
