"""
Uygulamanın giriş noktası: CLI veya Streamlit Web arayüzünü çalıştırır.
"""

import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def main():
    print("👨‍🍳 Recipe Agent'e Hoş Geldiniz!")
    print("Nasıl kullanmak istersiniz?")
    print("1. Terminal (CLI)")
    print("2. Web (Streamlit)")

    choice = input("Seçiminizi girin (1 veya 2): ").strip()

    if choice == "1":
        try:
            from ui.cli import run_cli
            logging.info("Terminal (CLI) arayüzü başlatılıyor.")
            run_cli()
        except Exception as e:
            logging.error(f"CLI başlatılamadı: {e}")
            print("️ Terminal arayüzü başlatılamadı.")

    elif choice == "2":
        try:
            import subprocess
            logging.info("Web arayüzü (Streamlit) başlatılıyor.")
            subprocess.run(["streamlit", "run", "ui/streamlit_ui.py"], check=True)
        except Exception as e:
            logging.error(f"Streamlit arayüzü başlatılamadı: {e}")
            print(" Web arayüzü başlatılamadı. Lütfen Streamlit'in kurulu olduğundan emin olun.")

    else:
        print(" Geçersiz seçim. Lütfen sadece 1 veya 2 girin.")
        logging.warning(f"Geçersiz seçim: {choice}")

if __name__ == "__main__":
    main()
