import requests

TOKEN = "8158114563:AAFmDhzCJGEwbv53Vgqw5ZeSKKXz-OZctfU"
CHAT_ID = "6003051424"

def mesaj_gonder(mesaj, gorsel_url=None):
    if gorsel_url and gorsel_url.startswith('//'):
        gorsel_url = 'https:' + gorsel_url
    
    if not gorsel_url or str(gorsel_url).lower() == "null":
        gorsel_url = None

    if gorsel_url:
        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
        payload = {"chat_id": CHAT_ID, "photo": gorsel_url, "caption": mesaj, "parse_mode": "HTML"}
    else:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": mesaj, "parse_mode": "HTML"}

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("[+] Telegram bildirimi gönderildi.")
        else:
            print(f"[!] Telegram Hatası ({response.status_code}): {response.text}")
            if gorsel_url:
                print("[*] Görsel gönderimi başarısız oldu, sadece metin deneniyor...")
                mesaj_gonder(mesaj, gorsel_url=None)
    except Exception as e:
        print(f"[!] Bağlantı hatası: {e}")