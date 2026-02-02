import time
from datetime import datetime
from helpers import price_extractor, stock_checker, converters, driver_factory, cookie_manager
import database

def kontrol_ve_analiz(url, size, urun_id=None, detay_goster=False, user_data=None):
    """
    ÖZELLİKLER:
    - Stok Hafızası: Ürün stoga girince (eskiden yoksa) bildirir.
    - İndirim Avı: İndirim varsa bildirir.
    - İlk Ekleme Kontrolü: Yeni eklenen ürüne gereksiz "Stok Geldi" demez.
    - İsim Güncelleme: Veritabanındaki isimsiz kayıtları düzeltir.
    - Detaylı CLI: Konsolda zengin görünüm sunar.
    """
    
    driver = driver_factory.create_driver()
    mesajlar = []
    
    try:
        driver.get(url)
        time.sleep(2) 
        
        try: cookie_manager.reject_cookies(driver)
        except: pass 

        data = price_extractor.get_product_data(driver)
        stok_durumu = stock_checker.check_stock(driver, size) 
        
        if urun_id and data["ad"] and data["ad"] != "İsim Bulunamadı":
            database.urun_guncelle(urun_id, data["ad"], data["renk"])

        yeni_float = converters.fiyat_to_float(data["yeni"])
        eski_float = converters.fiyat_to_float(data["eski"]) 
        
        if urun_id:
            db_son_fiyat = database.son_fiyati_getir(urun_id)
            db_float = converters.fiyat_to_float(db_son_fiyat)
            db_stok_durumu = database.son_stok_getir(urun_id)
        else:
            db_float = None
            db_stok_durumu = 0 
        
        ilk_kez_mi = (db_float is None)

        stok_var = stok_durumu["available"]
        indirim_var = (eski_float is not None and yeni_float is not None and eski_float > yeni_float)

        if detay_goster:
            simdi = datetime.now().strftime("%H:%M:%S")
            print(f"\n{'='*45}")
            print(f"🔍 [KONTROL - {simdi}]")
            print(f"📦 Ürün: {data['ad']} ({size})")
            
            if indirim_var:
                print(f"💰 Fiyat: {data['eski']} -> {data['yeni']} 🔥 (İNDİRİM!)")
            else:
                print(f"💰 Fiyat: {data['yeni']}")
            
            print(f"🚥 Durum: {stok_durumu['full_text']}")
            print(f"{'='*45}")
        
        mesaj = ""
        bildirim_yap = False

        if stok_var:
            
            if db_stok_durumu == 0 and not ilk_kez_mi:
                
                if indirim_var:
                    mesaj = (
                        f"🚨 <b>ALARM: BEDEN TEKRAR STOKLARDA!</b>\n"
                        f"🔥 <b>Üstelik İndirimli Fiyata!</b>\n\n"
                        f"📦 {data['ad']} ({size})\n"
                        f"💰 <b>{data['yeni']}</b> (<s>{data['eski']}</s>)\n"
                        f"🔗 <a href='{url}'>HEMEN SEPETE EKLE</a>"
                    )
                else: 
                    mesaj = (
                        f"✅ <b>MÜJDE: BEDEN TEKRAR STOKLARDA!</b>\n\n"
                        f"📦 {data['ad']} ({size})\n"
                        f"İstek listenizdeki ürünün bedeni geldi.\n"
                        f"💰 {data['yeni']}\n"
                        f"🔗 <a href='{url}'>HEMEN AL</a>"
                    )
                bildirim_yap = True
            
            elif indirim_var:
                if ilk_kez_mi or (db_float is None or yeni_float < db_float):
                    mesaj = (
                        f"🔥 <b>İSTEK LİSTENİZDEKİ ÜRÜN İNDİRİMDE!</b>\n"
                        f"Bedeniniz tükenmeden sepetinize ekleyin.\n\n"
                        f"📦 {data['ad']} ({size})\n"
                        f"💰 <b>{data['yeni']}</b> (<s>{data['eski']}</s>)\n"
                        f"🔗 <a href='{url}'>ÜRÜNE GİT</a>"
                    )
                    bildirim_yap = True

        if urun_id:
            database.fiyat_ve_stok_kaydet(urun_id, data["yeni"], stok_var)

        if bildirim_yap:
            mesajlar.append(mesaj)
            if detay_goster: 
                print("   🚀 Bildirim kuyruğa eklendi.")
        elif detay_goster:
             print("·············································")

        driver.quit() 
        return stok_var, data, mesajlar

    except Exception as e:
        print(f"⚠️ Analiz Hatası: {e}")
        try: driver.quit()
        except: pass
        return False, {"ad": "Hata", "yeni": "0", "gorsel": None, "renk": "Hata"}, []