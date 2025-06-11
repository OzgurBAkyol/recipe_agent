"""
Uygulamanın giriş noktası: CLI veya Streamlit Web arayüzünü çalıştırır.
"""

def main():
    print("👨‍🍳 Recipe Agent'e Hoş Geldiniz!")
    print("Nasıl kullanmak istersiniz?")
    print("1. Terminal (CLI)")
    print("2. Web (Streamlit)")
    choice = input("Seçiminizi girin (1 veya 2): ")

    if choice.strip() == "1":
        from ui.cli import run_cli
        run_cli()

    elif choice.strip() == "2":
        import os
        import subprocess
        print("🌐 Web arayüzü başlatılıyor...")
        subprocess.run(["streamlit", "run", "ui/streamlit_ui.py"])

    else:
        print("Geçersiz seçim. Lütfen 1 veya 2 girin.")

if __name__ == "__main__":
    main()
