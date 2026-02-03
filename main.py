import os
import sys
import database
from helpers import analyser, ui_tools, notifier, multi_tracker 

# Global session variable
# CURRENT_USER yapısı: (id, kullanici_adi, telegram_id)
CURRENT_USER = None  

def ekle_menu():
    """Yeni ürün ekleme ve ilk analiz."""
    print("\n" + "-"*20 + " YENİ ÜRÜN EKLE " + "-"*20)
    url = ui_tools.guvenli_input("🔗 Zara Ürün Linki: ", link_mi=True)
    size = ui_tools.guvenli_input("📏 Beden (S/M/L/XL/XXL): ").upper()
    
    # İsmi geçici olarak 'Analiz Ediliyor...' yapıyoruz
    u_id = database.urun_ekle(CURRENT_USER[0], "Analiz Ediliyor...", "...", url, size)
    
    print("\n[*] Ürün listeye eklendi, ilk kontrol yapılıyor...")
    
    try:
        stok, data, msgs = analyser.kontrol_ve_analiz(
            url, size, u_id, detay_goster=True, user_data=CURRENT_USER
        )
        for m in msgs:
            # GÜNCELLEME BURADA: Artık kullanıcının ID'sini (CURRENT_USER[2]) gönderiyoruz
            notifier.mesaj_gonder(CURRENT_USER[2], m, gorsel_url=data.get('gorsel'))
            
        print("\n✅ Ürün başarıyla kaydedildi.")
    except Exception as e:
        print(f"⚠️ İlk analizde hata: {e}")
    
    input("\n[↩] Devam etmek için Enter'a basın...")

def liste_menu():
    """Kullanıcının listesini gösterir."""
    urunler = database.urunleri_getir(CURRENT_USER[0])
    if not urunler:
        print("\n[!] Listeniz boş.")
    else:
        print("\n" + "="*20 + " TAKİP LİSTESİ " + "="*20)
        for u in urunler:
            print(f"[{u[0]}] {u[1]} ({u[4]}) - {u[2]}")
    
    input("\n[↩] Menüye dönmek için Enter...")

def sil_menu():
    """Ürün silme menüsü."""
    urunler = database.urunleri_getir(CURRENT_USER[0])
    if not urunler: 
        print("\n[!] Silinecek ürün yok."); input("[↩] Enter..."); return
    
    print("\n--- SİLME İŞLEMİ ---")
    for u in urunler: print(f"[{u[0]}] {u[1]} ({u[4]})")
    target = ui_tools.guvenli_input("\n🗑️ Silinecek Ürün ID (İptal için 0): ")
    if target != "0":
        database.urun_sil(target)
        print("✅ Ürün başarıyla silindi.")
        input("\n[↩] Devam etmek için Enter'a basın...")

def ana_menu():
    """Giriş sonrası ana yönetim ekranı."""
    global CURRENT_USER
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n║{'═'*43}║")
        print(f"║      💎 ZARA FIRSAT AVCISI v17.2          ║")
        print(f"║{'═'*43}║")
        print(f"👤 Aktif Kullanıcı: {CURRENT_USER[1]}")
        
        print("\n[1] 🚀 TAKİBİ BAŞLAT (Tüm Liste)")
        print("[2] 🆕 Yeni Ürün Ekle")
        print("[3] 📋 Listemi Gör")
        print("[4] 🗑️  Ürün Sil")
        print("[5] 🚪 Çıkış Yap")
        
        secim = ui_tools.guvenli_input("\n👉 Seçiminiz: ")

        if secim == "1": 
            # NOT: multi_tracker dosyanın içinde de 'notifier.mesaj_gonder' kullanıyorsan
            # oraya da CURRENT_USER[2] parametresini eklemeyi unutma!
            multi_tracker.baslat(CURRENT_USER)
            
        elif secim == "2": ekle_menu()
        elif secim == "3": liste_menu()
        elif secim == '4':
            print("\n-------------------- ÜRÜN SİL --------------------")
            urunler = database.urunleri_getir(CURRENT_USER[0])
            
            if not urunler:
                print("📭 Listeniz zaten boş.")
            else:
                print(f"{'ID':<5} {'Ürün Adı':<40} {'Beden'}")
                print("-" * 60)
                for u in urunler:
                    print(f"{u[0]:<5} {u[1][:38]:<40} {u[4]}")
                print("-" * 60)
                
                print("🚨 TÜM LİSTEYİ SİLMEK İÇİN '0' YAZIN.")
                
                silinecek = input("\n👉 Silinecek Ürün ID'si (İptal için Enter): ")
                
                if silinecek == '0':
                    onay = input("⚠️ DİKKAT: Tüm takip listeniz silinecek! Emin misiniz? (E/H): ").upper()
                    if onay == 'E':
                        database.tum_urunleri_sil(CURRENT_USER[0])
                        print("\n✅ Tüm liste başarıyla temizlendi.")
                    else:
                        print("\n❌ İşlem iptal edildi.")
                
                elif silinecek:
                    try:
                        database.urun_sil(int(silinecek))
                        print("\n✅ Ürün silindi.")
                    except:
                        print("\n❌ Hatalı ID girdiniz.")
            
            input("\n[↩] Menüye dönmek için Enter...")
        elif secim == "5": 
            CURRENT_USER = None
            break

def start_bot():
    """Programın ana giriş ve kayıt noktası."""
    global CURRENT_USER
    database.veritabani_hazirla()
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "═"*45)
        print("   🔑 ZARA BOT SİSTEM GİRİŞİ")
        print("═"*45)
        print("[1] Giriş Yap")
        print("[2] Yeni Kayıt Oluştur")
        print("[3] Programı Kapat")
        
        giris_secim = ui_tools.guvenli_input("\n👉 Seçiminiz: ")

        if giris_secim == "1":
            k_adi = ui_tools.guvenli_input("👤 Kullanıcı Adı: ")
            sifre = ui_tools.guvenli_input("🔐 Şifre: ")
            user = database.kullanici_giris(k_adi, sifre)
            if user:
                CURRENT_USER = user 
                ana_menu()
            else:
                print("\n[!] Hatalı kullanıcı adı veya şifre!")
                input("[↩] Tekrar denemek için Enter...")
        
        elif giris_secim == "2":
            print("\n" + "-"*15 + " YENİ KAYIT " + "-"*15)
            k_adi = ui_tools.guvenli_input("👤 Kullanıcı Adı: ")
            sifre = ui_tools.guvenli_input("🔐 Sistem Şifresi: ")
            
            # GÜNCELLEME BURADA: Zara bilgilerini sildik, sadece Telegram ID alıyoruz.
            t_id = ui_tools.guvenli_input("📱 Telegram ID: ")
            
            # Veritabanı kaydı (3 parametreli)
            if database.kullanici_kaydet(k_adi, sifre, t_id):
                print("\n✅ Kayıt başarılı! Şimdi giriş yapabilirsiniz.")
                input("[↩] Giriş ekranına dönmek için Enter...")
            else:
                print("\n[!] Bu kullanıcı adı zaten mevcut!")
                input("[↩] Tekrar denemek için Enter...")
        
        elif giris_secim == "3":
            print("\n[!] Program kapatılıyor. İyi avlar!"); 
            break

if __name__ == "__main__":
    start_bot()