def fiyat_to_float(fiyat):
    """
    Zara'nın '1.190,00 TL' formatındaki metinlerini sayısal float değerine dönüştürür.
    """
    if not fiyat or fiyat == "Okunamadı":
        return None
    try:
        return float(fiyat.replace("TL", "").replace(".", "").replace(",", ".").strip())
    except:
        return None