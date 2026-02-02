import sqlite3
from datetime import datetime

def veritabani_hazirla():
    conn = sqlite3.connect('takip.db', timeout=30, check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kullanicilar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kullanici_adi TEXT UNIQUE,
            sifre TEXT,
            telegram_id TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urunler (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            kullanici_id INTEGER,
            urun_adi TEXT,
            renk TEXT,
            url TEXT, 
            takip_beden TEXT,
            son_stok INTEGER DEFAULT 0, -- 0: Yok, 1: Var
            FOREIGN KEY (kullanici_id) REFERENCES kullanicilar (id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fiyat_gecmisi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            urun_id INTEGER,
            fiyat TEXT,
            tarih TEXT,
            FOREIGN KEY (urun_id) REFERENCES urunler (id)
        )
    """)
    
    cursor.execute("PRAGMA table_info(urunler)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'kullanici_id' not in columns:
        cursor.execute("ALTER TABLE urunler ADD COLUMN kullanici_id INTEGER")
    if 'renk' not in columns:
        cursor.execute("ALTER TABLE urunler ADD COLUMN renk TEXT")
    if 'urun_adi' not in columns:
        cursor.execute("ALTER TABLE urunler ADD COLUMN urun_adi TEXT")
    if 'son_stok' not in columns:
        cursor.execute("ALTER TABLE urunler ADD COLUMN son_stok INTEGER DEFAULT 0")
        
    conn.commit()
    conn.close()


def kullanici_kaydet(k_adi, sifre, t_id):
    """
    Yeni kayıt fonksiyonu.
    Artık z_email ve z_sifre almıyoruz.
    """
    try:
        conn = sqlite3.connect('takip.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO kullanicilar (kullanici_adi, sifre, telegram_id) 
            VALUES (?, ?, ?)
        """, (k_adi, sifre, t_id))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False 

def kullanici_giris(k_adi, sifre):
    """
    Giriş fonksiyonu.
    Dönen veri: (id, kullanici_adi, telegram_id)
    """
    conn = sqlite3.connect('takip.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, kullanici_adi, telegram_id FROM kullanicilar WHERE kullanici_adi = ? AND sifre = ?", (k_adi, sifre))
    user = cursor.fetchone()
    conn.close()
    return user 


def urun_ekle(kullanici_id, urun_adi, renk, url, beden):
    conn = sqlite3.connect('takip.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO urunler (kullanici_id, urun_adi, renk, url, takip_beden, son_stok) 
        VALUES (?, ?, ?, ?, ?, 0)
    """, (kullanici_id, urun_adi, renk, url, beden))
    urun_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return urun_id

def urunleri_getir(kullanici_id):
    conn = sqlite3.connect('takip.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, urun_adi, renk, url, takip_beden FROM urunler WHERE kullanici_id = ?", (kullanici_id,))
    veriler = cursor.fetchall()
    conn.close()
    return veriler

def fiyat_kaydet(urun_id, yeni_fiyat):
    """Sadece fiyat geçmişine ekleme yapar."""
    conn = sqlite3.connect('takip.db')
    cursor = conn.cursor()
    tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO fiyat_gecmisi (urun_id, fiyat, tarih) VALUES (?, ?, ?)", 
                   (urun_id, yeni_fiyat, tarih))
    conn.commit()
    conn.close()

def fiyat_ve_stok_kaydet(urun_id, yeni_fiyat, stok_var_mi):
    """
    Hem fiyatı geçmişe kaydeder HEM DE 'son_stok' durumunu günceller.
    """
    conn = sqlite3.connect('takip.db')
    cursor = conn.cursor()
    
    tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stok_int = 1 if stok_var_mi else 0
    
    cursor.execute("INSERT INTO fiyat_gecmisi (urun_id, fiyat, tarih) VALUES (?, ?, ?)", 
                   (urun_id, yeni_fiyat, tarih))
    
    cursor.execute("UPDATE urunler SET son_stok = ? WHERE id = ?", (stok_int, urun_id))
    
    conn.commit()
    conn.close()

def son_fiyati_getir(urun_id):
    conn = sqlite3.connect('takip.db')
    cursor = conn.cursor()
    cursor.execute("SELECT fiyat FROM fiyat_gecmisi WHERE urun_id = ? ORDER BY id DESC LIMIT 1", (urun_id,))
    res = cursor.fetchone()
    conn.close()
    return res[0] if res else None

def son_stok_getir(urun_id):
    """
    Ürünün veritabanındaki son stok durumunu getirir (0 veya 1).
    """
    conn = sqlite3.connect('takip.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT son_stok FROM urunler WHERE id = ?", (urun_id,))
        res = cursor.fetchone()
        return res[0] if res else 0
    except:
        return 0
    finally:
        conn.close()

def urun_sil(urun_id):
    conn = sqlite3.connect('takip.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM urunler WHERE id = ?", (urun_id,))
    cursor.execute("DELETE FROM fiyat_gecmisi WHERE urun_id = ?", (urun_id,))
    conn.commit()
    conn.close()

def urun_guncelle(urun_id, yeni_ad, yeni_renk):
    conn = sqlite3.connect('takip.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE urunler SET urun_adi = ?, renk = ? WHERE id = ?", (yeni_ad, yeni_renk, urun_id))
    conn.commit()
    conn.close()

def tum_urunleri_sil(kullanici_id):
    """
    Kullanıcının tüm takip listesini ve fiyat geçmişini siler (Toplu Silme).
    """
    conn = sqlite3.connect('takip.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        DELETE FROM fiyat_gecmisi 
        WHERE urun_id IN (SELECT id FROM urunler WHERE kullanici_id = ?)
    """, (kullanici_id,))
    
    cursor.execute("DELETE FROM urunler WHERE kullanici_id = ?", (kullanici_id,))
    
    conn.commit()
    conn.close()