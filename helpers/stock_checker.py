from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def check_stock(driver, target_size):
    """
    Zara stok kontrolü yapar.
    - 'Benzer Ürünler' tuzağını yakalar.
    - S/XS/Small karışıklığını önler (Tam kelime eşleşmesi).
    - Gizli menüleri açmak için sepete ekle butonunu tetikler.
    """
    result = {
        "available": False,
        "full_text": "❌ BEDEN LİSTESİ BULUNAMADI"
    }

    try:
        target = target_size.strip().upper()
        
        try:
            add_btn = driver.find_elements(By.CSS_SELECTOR, "button[data-qa-action='add-to-cart']")
            if add_btn:
                driver.execute_script("arguments[0].click();", add_btn[0])
                time.sleep(1) 
        except:
            pass

        selectors = [
            "li.product-detail-size-selector__size-list-item",     
            "ul[class*='size-selector'] > li",                     
            "div.product-detail-size-selector__size-list-item",    
            "button[class*='size-selector']"                       
        ]

        elements = []
        for sel in selectors:
            found = driver.find_elements(By.CSS_SELECTOR, sel)
            elements.extend(found)

        if not elements:
            return result

        for el in elements:
            try:
                visible_text = el.text.replace('\n', ' ').strip().upper()
                data_name = el.get_attribute("data-name")
                data_name = data_name.upper() if data_name else ""
                
                full_text_search = f"{visible_text} {data_name}"

                kelimeler = full_text_search.replace('(', ' ').replace(')', ' ').split()

                if target in kelimeler:
                    
                    if "BENZER" in full_text_search or "SIMILAR" in full_text_search or "COMING SOON" in full_text_search or "GELECEK" in full_text_search:
                        return {"available": False, "full_text": f"❌ STOK YOK (Benzer/Gelecek)"}

                    classes = (el.get_attribute("class") or "").lower()
                    if "disabled" in classes or "out-of-stock" in classes:
                        return {"available": False, "full_text": "❌ TÜKENDİ"}

                    try:
                        parent = el.find_element(By.XPATH, "./..")
                        p_classes = (parent.get_attribute("class") or "").lower()
                        if "disabled" in p_classes:
                            return {"available": False, "full_text": "❌ TÜKENDİ"}
                    except:
                        pass

                    return {"available": True, "full_text": f"✅ STOKTA ({visible_text})"}

            except Exception:
                continue

        return {"available": False, "full_text": "❌ BEDEN LİSTEDE YOK"}

    except Exception as e:
        print(f"⚠️ Stok kontrol hatası: {e}")
        return {"available": False, "full_text": "⚠️ HATA OLUŞTU"}