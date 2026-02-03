import time
import concurrent.futures
import database
from helpers import analyser, ui_tools, notifier

def tekli_urun_kontrolu(urun, current_user):
    """
    Multi-thread havuzunda çalışacak olan tekil kontrol fonksiyonu.
    urun: (id, kullanici_id, urun_adi, renk, url, takip_beden)
    """
    try:
        u_id = urun[0]
        u_ad = urun[1] 
        url = urun[3]   
        beden = urun[4] 
        
        print(f"🔎 Kontrol Ediliyor: {u_ad} ({beden})")
        
        stok, data, indirim_mesajlari = analyser.kontrol_ve_analiz(
            url, beden, u_id, detay_goster=True, user_data=current_user
        )
        
        for m in indirim_mesajlari:
            notifier.mesaj_gonder(current_user[2], m, gorsel_url=data.get('gorsel'))
            
        return True
    except Exception as e:
        print(f"❌ HATA ({urun[1]}): {e}")
        return False

def baslat(current_user):
    """
    Tüm listeyi Multi-Thread ile tarayan ana fonksiyon.
    Main dosyasından sadece bu çağrılır.
    """
    if not current_user:
        print("⚠️ Oturum hatası: Kullanıcı bulunamadı.")
        return

    print(f"\n🚀 TAKİP MODU BAŞLATILIYOR...")
    print(f"👤 Kullanıcı: {current_user[1]}")
    
    try:
        dakika = int(ui_tools.guvenli_input("⏱️ Tur aralığı (Dakika): "))
    except ValueError:
        print("⚠️ Geçersiz sayı, varsayılan olarak 5 dakika ayarlandı.")
        dakika = 5
    
    MAX_ISCI = 4 
    
    print(f"\n⚡ Multi-Thread Modu Aktif: Aynı anda {MAX_ISCI} ürün taranacak.")
    
    while True:
        try:
            urunler = database.urunleri_getir(current_user[0])
            
            if not urunler:
                print("\n[!] Listeniz boş! Önce ana menüden ürün ekleyin.")
                break
            
            print(f"\n" + "="*40)
            print(f"🔄 TUR BAŞLIYOR - Toplam Ürün: {len(urunler)}")
            print("="*40)

            with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_ISCI) as executor:
                gelecek_gorevler = {
                    executor.submit(tekli_urun_kontrolu, urun, current_user): urun 
                    for urun in urunler
                }
                
                for future in concurrent.futures.as_completed(gelecek_gorevler):
                    try:
                        future.result()
                    except Exception as e:
                        print(f"⚠️ Thread Hatası: {e}")
            
            print("\n✅ Tur tamamlandı.")
            
            ui_tools.bekleme_animasyonu(dakika)
                
        except KeyboardInterrupt:
            print("\n" + "!"*10 + " TAKİP DURDURULDU " + "!"*10)
            break 
        except Exception as e:
            print(f"\n[!] Beklenmedik Döngü Hatası: {e}")
            time.sleep(5)