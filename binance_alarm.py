import requests
import time

# ================== AYARLAR ==================
BOT_TOKEN = "8217229216:AAHsMyjGMtZKw6FXuPKRsgY_ydgqNXbE2VE"
CHAT_ID = "-1003829375204"

PERCENT_LIMIT = 15        # %20 artış
CHECK_INTERVAL = 30       # saniye (1 dk)
# ============================================

BINANCE_API = "https://api.binance.com/api/v3/ticker/price"

last_prices = {}
alerted = set()


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)


print("🚀 Binance USDT %20 alarm sistemi başladı...")

while True:
    try:
        response = requests.get(BINANCE_API, timeout=10)
        data = response.json()

        for coin in data:
            symbol = coin["symbol"]

            # SADECE USDT PARİTELERİ
            if not symbol.endswith("USDT"):
                continue

            price = float(coin["price"])

            if symbol not in last_prices:
                last_prices[symbol] = price
                continue

            old_price = last_prices[symbol]
            if old_price == 0:
                last_prices[symbol] = price
                continue

            change = ((price - old_price) / old_price) * 100

            if change >= PERCENT_LIMIT and symbol not in alerted:
                message = (
                    f"🚀 {symbol}\n"
                    f"%{change:.2f} YÜKSELDİ\n"
                    f"Eski: {old_price}\n"
                    f"Yeni: {price}"
                )
                send_telegram(message)
                alerted.add(symbol)

            last_prices[symbol] = price

        time.sleep(CHECK_INTERVAL)

    except Exception as e:
        print("Hata:", e)
        time.sleep(10)
