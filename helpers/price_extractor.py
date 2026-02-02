def get_product_data(driver):
    try:
        script = """
            function getBestImage() {
                var ogImg = document.querySelector('meta[property="og:image"]');
                if (ogImg && ogImg.content && ogImg.content.startsWith('http')) return ogImg.content;

                var source = document.querySelector('.product-detail-images__image source');
                if (source && source.srcset) {
                    var urls = source.srcset.split(',');
                    return urls[urls.length - 1].trim().split(' ')[0];
                }

                var img = document.querySelector('.product-detail-images__image img');
                return img ? img.src : null;
            }

            function getProductColor() {
                var colorSelectors = [
                    '.product-detail-info__color',
                    '.product-detail-color-selector__selected-color-name',
                    'span[class*="color-name"]',
                    '.product-color'
                ];
                
                for (var sel of colorSelectors) {
                    var el = document.querySelector(sel);
                    if (el && el.innerText.trim()) {
                        return el.innerText.replace("Renk: ", "").trim();
                    }
                }
                return "Belirlenemedi";
            }

            var nameEl = document.querySelector('.product-detail-info__header-name, h1');
            var discountEl = document.querySelector('ins .money-amount--highlight .money-amount__main');
            var oldEl = document.querySelector('del .money-amount__main');
            var normalEl = document.querySelector('.money-amount__main');

            function clean(el) {
                return el ? el.innerText.replace(/\\s+/g, ' ').trim() : null;
            }

            var yeni = clean(discountEl) || clean(normalEl) || 'Okunamadı';
            var eski = clean(oldEl);
            
            if (discountEl && clean(normalEl) !== yeni) {
                eski = clean(normalEl);
            }

            return {
                "ad": clean(nameEl) || "İsim Bulunamadı",
                "renk": getProductColor(),
                "eski": eski,
                "yeni": yeni,
                "gorsel": getBestImage()
            };
        """
        return driver.execute_script(script)
    except:
        return {"ad": "Hata", "renk": "Hata", "eski": None, "yeni": "Okunamadı", "gorsel": None}