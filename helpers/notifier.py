import requests
import sys
import os

# config.py dosyasını bulmak için yol eklemesi
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import config
    TOKEN = config.TELEGRAM_TOKEN
except ImportError:
    print("⚠️ UYARI: config.py dosyası bulunamadı!")
    TOKEN = None

# ARTIK CHAT_ID'Yİ DIŞARIDAN ALIYORUZ
def mesaj_gonder(chat_id, mesaj, gorsel_url=None):
    if not TOKEN:
        print("❌ HATA: Token bulunamadı.")
        return

    # Görsel URL düzeltmeleri
    if gorsel_url and gorsel_url.startswith('//'):
        gorsel_url = 'https:' + gorsel_url
    if not gorsel_url or str(gorsel_url).lower() == "null":
        gorsel_url = None

    if gorsel_url:
        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
        payload = {"chat_id": chat_id, "photo": gorsel_url, "caption": mesaj, "parse_mode": "HTML"}
    else:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": mesaj, "parse_mode": "HTML"}

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("[+] Telegram bildirimi gönderildi.")
        else:
            print(f"[!] Telegram Hatası ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"[!] Bağlantı hatası: {e}")