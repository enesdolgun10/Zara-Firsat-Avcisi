# 💎 Zara Fırsat Avcısı (Zara Opportunity Hunter)

Zara Fırsat Avcısı, **Zara'nın web sitesindeki ürünlerin fiyat ve stok durumlarını 7/24 takip eden**, indirim veya stok geldiğinde size **anında Telegram üzerinden bildirim gönderen** akıllı bir bottur.

> İstediğiniz ürünü bedeniyle birlikte ekleyin, bot sizin yerinize nöbet tutsun! 🚀

---

## 🎯 Projenin Amacı

Zara'da çok beğendiğiniz bir ürünün bedeni mi kalmadı?  
Ya da indirime girmesini mi bekliyorsunuz?

Sürekli sayfayı yenilemek yerine bu botu çalıştırın.

### Botun Yetenekleri

- **📦 Stok Takibi**  
  Stokta olmayan ürünleri izler, stok geldiği an  
  _"Benzer Ürünler" tuzağına düşmeden_ size haber verir.

- **💸 İndirim Yakalama**  
  Fiyat değişimlerini izler, indirim olduğunda anında bildirir.

- **🧠 Akıllı Hafıza**  
  Ürün stoktan gidip geri gelirse tekrar hatırlatır.

---

## 🛠️ Kullanılan Teknolojiler ve Kütüphaneler

Bu proje **Python** ile geliştirilmiştir ve aşağıdaki teknolojileri kullanır:

- **Selenium & Undetected Chromedriver**  
  Zara'nın bot korumasını aşmak ve siteyi gerçek bir insan gibi gezmek için.

- **SQLite**  
  Ürün listenizi, kullanıcı bilgilerinizi ve fiyat geçmişini saklamak için.

- **Requests**  
  Telegram API ile iletişim kurmak için.

- **Multi-Threading**  
  Aynı anda birden fazla ürünü hızlıca taramak için.

---

## 🚀 Kurulum ve Kullanım (Adım Adım)

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları takip edin.

### 1️⃣ Projeyi İndirin

Terminali açın ve projeyi bilgisayarınıza çekin:

```bash
git clone https://github.com/KULLANICI_ADINIZ/zara-firsat-avcisi.git
cd zara-firsat-avcisi
```

### 2️⃣ Gerekli Kütüphaneleri Yükleyin

Python'un yüklü olduğundan emin olun, ardından kütüphaneleri kurun:

```bash
pip install -r requirements.txt
```

### 3️⃣ Telegram Botunuzu Oluşturun

Bildirim alabilmek için kendi botunuzu oluşturmalısınız:

1. Telegram'da **@BotFather** kullanıcısını bulun.
2. `/newbot` komutunu gönderin ve bota bir isim verin.
3. Size verilen **HTTP API Token**'ı kopyalayın.

### 4️⃣ Config Dosyasını Ayarlayın

Proje klasöründeki `config_ornek.py` dosyasının adını `config.py` olarak değiştirin.

```text
Eski Adı: config_ornek.py
Yeni Adı: config.py
```

Dosya içeriği:

```python
# config.py
TELEGRAM_TOKEN = "BURAYA_BOTFATHERDAN_ALDIGINIZ_TOKENI_YAPISTIRIN"
```

### 5️⃣ Botu Çalıştırın

Her şey hazır! Şimdi botu başlatın:

```bash
python main.py
```

---

## 📱 Nasıl Kullanılır?

1. **Kayıt Olun**  
   Program açıldığında `[2] Yeni Kayıt Oluştur` seçeneğine girin.  
   Kullanıcı adı, şifre ve **Telegram ID** girin.  
   (Telegram ID öğrenmek için: **@userinfobot**)

2. **Giriş Yapın**  
   Kayıt sonrası giriş yapın.

3. **Ürün Ekleyin**  
   Menüden ürün ekle diyerek **Zara ürün linkini** ve **bedenini** girin.

4. **Takibi Başlatın**  
   `[1] Takibi Başlat` seçeneği ile botu çalıştırın.  
   Bot arka planda çalışır ve size **Telegram üzerinden fotoğraf + bilgi** gönderir.

---

## 🔮 Gelecek Planları (To-Do)

Bu proje şu an temel işlevlerini sorunsuz yerine getirmektedir ancak geliştirmeye açıktır.

Planlanan özellikler:

- [ ] 🌐 Web Arayüzü (GUI) – Terminal yerine modern bir arayüz
- [ ] 🌍 Çoklu Dil Desteği – Farklı ülkelerdeki Zara mağazaları
- [ ] 🛡️ Proxy Desteği – IP ban riskini azaltmak için
- [ ] 💬 Discord Entegrasyonu – Bildirimleri Discord'dan alma

---

## ⚠️ Yasal ve Kullanım Notu

> Bu proje **eğitim ve kişisel kullanım** amaçlı geliştirilmiştir.  
> Ticari kullanım ve Zara'nın kullanım şartlarına aykırı işlemler kullanıcı sorumluluğundadır.

---

## 🏹 İyi Avlar!
