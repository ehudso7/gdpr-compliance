from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import logging

logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s %(levelname)s:%(message)s')

def check_gdpr_compliance(url):
    try:
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get(url)
        has_cookie_banner = "cookie" in driver.page_source.lower()
        has_privacy_policy = "privacy policy" in driver.page_source.lower()
        driver.quit()
        result = {"cookie_banner": has_cookie_banner, "privacy_policy": has_privacy_policy}
        logging.info(f"Compliance check for {url}: {result}")
        return result
    except Exception as e:
        logging.error(f"Error checking {url}: {str(e)}")
        return {"error": str(e)}
