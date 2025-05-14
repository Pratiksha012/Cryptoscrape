# 🪙 Real-Time Cryptocurrency Data Ingestion Pipeline

This project is a **real-time data engineering pipeline** that scrapes live cryptocurrency data from [CoinMarketCap](https://coinmarketcap.com) using **Selenium**, and stores the cleaned data in both **PostgreSQL** and **MongoDB** databases. The system is designed to run continuously in the background using `nohup`, enabling seamless, long-running ingestion of dynamic web data.

---

## 🚀 Key Features

- 🔄 **Automated Web Scraping:** Scrapes live market price, hourly and daily percentage changes, and market cap from CoinMarketCap using Selenium with ChromeDriver.
- 🧹 **Data Validation & Deduplication:** Checks for repeated entries before storing to avoid redundancy.
- 🧱 **Dual Storage Design:**
  - **PostgreSQL:** For structured, relational storage and SQL querying.
  - **MongoDB:** For flexible, schema-less NoSQL storage and rapid access.
- 👻 **Daemonized Process:** Designed to run indefinitely in the background using `nohup`, minimizing manual monitoring.
- 🕓 **Timestamped Records:** Every entry is timestamped to maintain a clean historical timeline of market changes.

---

## 🧩 Technologies Used

- Python 3.x  
- Selenium WebDriver  
- ChromeDriver Manager  
- PostgreSQL  
- MongoDB  
- psycopg2  
- pymongo  
- nohup (Unix shell command)

---

