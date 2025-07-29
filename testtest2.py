import requests
import time
from bs4 import BeautifulSoup

URL = "https://funpay.com/lots/3386/"  # Раздел Roblox - Grow a Garden
CHECK_INTERVAL = 30  # секунд

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1397038122826600630/UHjN-cFelC3VckRCletTwFQN28X0QjaFYEPGTRsbJMLB-xDYsu-0MQ9sMXHm9TW5OS9a"

WANTED_ITEMS = {
    "kitsune": 170,
    "raccoon": 400,
    "енот": 400,
    "Butterfly": 330,
    "Disco bee": 540,
    "dragonfly": 120,
    "стрекоза": 120,
    "red fox": 30,
    "лиса": 30
}

FORBIDDEN_WORDS = ["фарм", "сундук", "гайд", "кейс", "egg", "яйцо", "tanuki", "афк", "ваш", "как", "наложу", "chest"]

seen = set()

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def parse_price(price_str):
    try:
        return float(price_str.replace("₽", "").replace(",", ".").strip())
    except:
        return None


def contains_forbidden(title):
    title_lower = title.lower()
    return any(word in title_lower for word in FORBIDDEN_WORDS)


def is_wanted(title, price):
    title_lower = title.lower()
    if contains_forbidden(title_lower):
        return False
    for keyword, max_price in WANTED_ITEMS.items():
        if keyword in title_lower and price is not None and price <= max_price:
            return True
    return False


def send_to_discord(title, price, href):
    url = f"https://funpay.com{href}" if href.startswith("/") else href
    payload = {
        "content": f"{title}\n{url}\n{price} ₽\n@everyone"
    }
    try:
        res = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        print(f"📤 Отправлено в Discord: {title} | {price} ₽ | Статус: {res.status_code}")
    except Exception as e:
        print("❌ Ошибка при отправке в Discord:", e)


def main():
    print("✅ Скрипт запущен и следит за лотами...")
    while True:
        try:
            response = requests.get(URL, headers=HEADERS)
            soup = BeautifulSoup(response.text, "html.parser")
            items = soup.select("a.tc-item")

            for item in items:
                title = item.get("title") or item.text
                cost_tag = item.select_one(".tc-price")
                link = item.get("href")
                price_str = cost_tag.text.strip() if cost_tag else ""
                price = parse_price(price_str)

                if not title or not price or not link:
                    continue

                uid = f"{title}|{price}|{link}"
                if uid in seen:
                    continue

                if is_wanted(title, price):
                    send_to_discord(title, price, link)
                    seen.add(uid)
                else:
                    print(f"🔍 Не прошло фильтр: {title} | {price} ₽")

        except Exception as e:
            print("❌ Ошибка во время обработки:", e)

        print(f"⏳ Ожидание {CHECK_INTERVAL} сек...\n")
        time
