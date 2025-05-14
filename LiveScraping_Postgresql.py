from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import psycopg2
from datetime import datetime

# PostgreSQL Connection
conn = psycopg2.connect(
    dbname="YOUR_DBNAME",
    user="YOUR_USERNAME",
    password="YOUR_PASSWORD",
    host="localhost",
    port="5433"
)
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS crypto_prices (
        id SERIAL PRIMARY KEY,
        price TEXT,
        change_1h TEXT,
        change_24h TEXT,
        market_cap TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

# Selenium WebDriver setup
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

        current_timestamp = datetime.now()

        # Check if the last stored entry is the same
        cursor.execute("""
            SELECT price, change_1h, change_24h, market_cap FROM crypto_prices 
            ORDER BY timestamp DESC LIMIT 1
        """)
        last_entry = cursor.fetchone()

        if last_entry and last_entry == (price, change_1h, change_24h, market_cap):
            print(f"No change in data at {current_timestamp}, skipping insert.")
            return

        # Insert new data
        cursor.execute("""
            INSERT INTO crypto_prices (price, change_1h, change_24h, market_cap, timestamp) 
            VALUES (%s, %s, %s, %s, %s)
        """, (price, change_1h, change_24h, market_cap, current_timestamp))
        conn.commit()
        print(f"Stored in DB at {current_timestamp}: {price}, {change_1h}, {change_24h}, {market_cap}")

    except Exception as e:
        print(f"Error at {datetime.now()}: {e}")

try:
    while True:
        scrape_crypto_prices()
        time.sleep(1)  # Fetch data every minute
finally:
    driver.quit()
    cursor.close()
    conn.close()
