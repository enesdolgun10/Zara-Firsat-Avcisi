import sys
import time

def bekleme_animasyonu(dakika):
    toplam_saniye = dakika * 60
    print(f"\n[*] Bir sonraki kontrol için {dakika} dakika bekleniyor...")
    for kalan in range(toplam_saniye, 0, -1):
        try:
            dakika_kalan, saniye_kalan = kalan // 60, kalan % 60
            ilerleme = int(((toplam_saniye - kalan) / toplam_saniye) * 20)
            cubuk = "█" * ilerleme + "-" * (20 - ilerleme)
            sys.stdout.write(f"\r[{cubuk}] {dakika_kalan:02d}:{saniye_kalan:02d} kaldı | Çıkış: Ctrl+C")
            sys.stdout.flush()
            time.sleep(1)
        except KeyboardInterrupt:
            raise KeyboardInterrupt
    print("\n" + "-" * 40 + "\n[*] Süre doldu, kontrol başlıyor...\n")

def guvenli_input(mesaj, link_mi=False):
    while True:
        try:
            deger = input(mesaj).strip().replace('"', '')
            if not deger: continue
            yasakli = ["activate", "venv", "scripts", "ps1", "python.exe", "& c:"]
            if any(x in deger.lower() for x in yasakli): continue
            if link_mi:
                if "zara.com" in deger and deger.startswith("http"): return deger
                print("[!] Geçersiz Zara linki!"); continue
            return deger
        except KeyboardInterrupt:
            onay = input("\n[?] Programı kapatmak istiyor musunuz? (E/H): ").lower()
            if onay == 'e': sys.exit()
            else: continue