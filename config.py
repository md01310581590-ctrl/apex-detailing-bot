import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
try:
    ADMIN_ID = int(os.getenv("ADMIN_ID", "1850174341").strip())
except ValueError:
    ADMIN_ID = 1850174341

DB_PATH = BASE_DIR / "detailing_demo.db"

# Студия разработчик (для водяных знаков и продажи решения)
DEV_CHANNEL = "@pxlbot_studios"
DEV_BOT = "@pxlbot_studios_bot"
DEV_CONTACT = "@Nicky_pxl"

# Классы автомобилей и базовые коэффициенты
CAR_CLASSES = {
    "sedan": {
        "title": "🏎 Седан / Купе / Лифтбек",
        "examples": "BMW 3/5, Porsche 911, Zeekr 001, Audi A6",
        "mult": 1.0
    },
    "crossover": {
        "title": "🚙 Кроссовер / Compact SUV",
        "examples": "BMW X3/X5, Geely Monjaro, Porsche Cayenne, Macan",
        "mult": 1.2
    },
    "large_suv": {
        "title": "🚐 Большой внедорожник / Минивэн",
        "examples": "Li Auto L9, Toyota LC300, Cadillac Escalade, V-Class",
        "mult": 1.4
    }
}

# Пакеты услуг
SERVICES = {
    "risk_zones": {
        "title": "🛡 Пакет «Зоны риска» (Полиуретан)",
        "base_min": 65000,
        "base_max": 80000,
        "time": "1-2 дня",
        "desc": "Капот целиком, передний бампер, оптика, крылья, зеркала, полоса на крышу, зоны под ручками. Пленка 200 мкм (SunTek / Stek) с самозатягивающимся слоем."
    },
    "full_poly": {
        "title": "💎 Полная оклейка кузова (Полиуретан глянец/мат)",
        "base_min": 180000,
        "base_max": 220000,
        "time": "4-5 дней",
        "desc": "100% защита всех окрашенных элементов кузова премиальным полиуретаном 200-215 мкм с гидрофобным top-coat. Защита от гравия, притертостей, реагентов и пескоструя. Гарантия 7 лет."
    },
    "ceramic": {
        "title": "✨ Керамика (Глубокая полировка + 2+1 слой)",
        "base_min": 45000,
        "base_max": 55000,
        "time": "2 дня",
        "desc": "Мягкая восстановительная полировка (удаление до 90% царапин и паутинки) + 2 слоя керамики 9H + гидрофобный слой. Зеркальный блеск и защита от дорожной химии на 1,5 года."
    },
    "dry_clean": {
        "title": "🧼 Детейлинг салона + Консервация кожи",
        "base_min": 25000,
        "base_max": 32000,
        "time": "1-2 дня",
        "desc": "Полный разбор и деликатная химчистка всех поверхностей (пар, экстрактор), озонирование, пропитка премиальной кожи защитными кремами от растрескивания и заломов."
    }
}
