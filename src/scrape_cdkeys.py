import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import matplotlib.pyplot as plt
import schedule
import time

DB_FILE = "cdkeys_prices.db"
GAME_NAME = "Persona 5 Royal (PC)"
GAME_URL = "https://www.cdkeys.com/persona-5-royal-pc-steam"  # ตัวอย่าง URL

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS prices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    game_name TEXT,
                    price REAL,
                    timestamp TEXT
                )''')
    conn.commit()
    conn.close()

def scrape_price():
    try:
        r = requests.get(GAME_URL, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        price_tag = soup.select_one('meta[itemprop="price"]')
        if price_tag:
            price = float(price_tag["content"])
            ts = datetime.now().isoformat(sep=" ", timespec="seconds")
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("INSERT INTO prices (game_name, price, timestamp) VALUES (?, ?, ?)",
                      (GAME_NAME, price, ts))
            conn.commit()
            conn.close()
            print(f"✅ {GAME_NAME}: {price} THB @ {ts}")
        else:
            print("⚠️ ไม่พบแท็กราคา")
    except Exception as e:
        print(f"❌ Error: {e}")

def plot_graph():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT timestamp, price FROM prices WHERE game_name=?", (GAME_NAME,))
    rows = c.fetchall()
    conn.close()
    
    if not rows:
        print("⚠️ ไม่มีข้อมูลใน DB")
        return
    
    times = [datetime.fromisoformat(r[0]) for r in rows]
    prices = [r[1] for r in rows]
    
    plt.figure(figsize=(10,5))
    plt.plot(times, prices, marker='o', label=GAME_NAME)
    plt.xlabel("เวลา")
    plt.ylabel("ราคา (THB)")
    plt.title(f"แนวโน้มราคา: {GAME_NAME}")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("price_graph.png")
    plt.close()
    print("📊 กราฟบันทึกเป็น price_graph.png แล้ว")

if __name__ == "__main__":
    init_db()
    scrape_price()
    schedule.every(1).hours.do(scrape_price)
    schedule.every().day.at("23:59").do(plot_graph)

    while True:
        schedule.run_pending()
        time.sleep(1)