import undetected_chromedriver as uc
import threading 

DRIVER_CREATION_LOCK = threading.Lock()

def create_driver():
    """
    Multi-Thread uyumlu, dosya çakışmasını engelleyen driver oluşturucu.
    """
    options = uc.ChromeOptions()
    
    options.add_argument("--window-position=-10000,0") 
    options.add_argument("--remote-debugging-port=0")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-popup-blocking")
    
    options.add_argument("--no-first-run")
    options.add_argument("--password-store=basic")
    
    with DRIVER_CREATION_LOCK:
        try:
            driver = uc.Chrome(
                options=options, 
                headless=False, 
                use_subprocess=True, 
                version_main=144
            )
        except TypeError:
            driver = uc.Chrome(options=options, headless=False, version_main=144)
    
    return driver