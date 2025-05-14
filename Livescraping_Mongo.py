from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pymongo
from datetime import datetime

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["crypto_db"]
collection = db["crypto_prices"]

options = Options()
options.add_argument("--headless") 
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

URL = "https://coinmarketcap.com/"

def scrape_crypto_prices():
    driver.get(URL)
    time.sleep(5)

    try:
        wait = WebDriverWait(driver, 15) 
        try:
            price_tag = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class, 'sc-142c02c-0') and contains(@class, 'lmjbLF')]")
            ))
            price = price_tag.text.strip()
        except:
            price = "N/A"

        try:
            change_1h_tag = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//span[contains(@class, 'sc-1e8091e1-0') and contains(@class, 'jgYsZM')]")
            ))
            change_1h = change_1h_tag.text.strip()
        except:
            change_1h = "N/A"

        try:
            change_24h_tag = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//span[contains(@class, 'sc-1e8091e1-0') and contains(@class, 'jgYsZM')]")
            ))
            change_24h = change_24h_tag.text.strip()
        except:
            change_24h = "N/A"

        try:
            market_cap_tag = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//span[contains(@class, 'sc-11478e5d-1') and contains(@class, 'jfwGHx')]")
            ))
            market_cap = market_cap_tag.text.strip()
        except:
            market_cap = "N/A"

        current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        last_entry = collection.find_one(sort=[("timestamp", -1)])

        if (last_entry and 
            last_entry["price"] == price and 
            last_entry["change_1h"] == change_1h and 
            last_entry["change_24h"] == change_24h and 
            last_entry["market_cap"] == market_cap):
            print(f"No change in data at {current_timestamp}, skipping insert.")
            return

        data = {
            "price": price,
            "change_1h": change_1h,
            "change_24h": change_24h,
            "market_cap": market_cap,
            "timestamp": current_timestamp 
        }

        collection.insert_one(data)
        print(f"Stored in DB at {current_timestamp}: {data}")

    except Exception as e:
        print(f"Error at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {e}")

try:
    while True:
        scrape_crypto_prices()
        time.sleep(1)
finally:
    driver.quit()
