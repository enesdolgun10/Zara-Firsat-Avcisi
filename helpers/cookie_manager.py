def reject_cookies(driver):
    """
    Zara'nın çerez uyarısını JavaScript ile zorla kapatır.
    """
    try:
        driver.execute_script("""
            // 'Tümünü Reddet' butonu varsa tıkla
            var btn = document.getElementById('onetrust-reject-all-handler');
            if(btn) btn.click();
            else {
                // Buton yoksa tüm paneli (SDK) sil ve sayfayı kaydırılabilir yap
                var sdk = document.getElementById('onetrust-consent-sdk');
                if(sdk) { sdk.remove(); document.body.style.overflow = 'auto'; }
            }
        """)
    except Exception as e:
        print(f"[-] Çerez hatası: {e}")