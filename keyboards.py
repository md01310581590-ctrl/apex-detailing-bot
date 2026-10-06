from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from config import CAR_CLASSES, SERVICES, DEV_CONTACT, DEV_CHANNEL, DEV_BOT

def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⚡ Рассчитать стоимость (20 сек)")],
            [KeyboardButton(text="📸 Портфолио: ДО / ПОСЛЕ"), KeyboardButton(text="🛡 Материалы и Гарантия")],
            [KeyboardButton(text="📍 Локация и Боксы"), KeyboardButton(text="🛠 Заказать такой бот себе")]
        ],
        resize_keyboard=True
    )

def car_classes_keyboard() -> InlineKeyboardMarkup:
    buttons = []
    for code, data in CAR_CLASSES.items():
        buttons.append([InlineKeyboardButton(text=data["title"], callback_data=f"class:{code}")])
    buttons.append([InlineKeyboardButton(text="« Назад в главное меню", callback_data="to_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def quick_models_keyboard(car_class: str) -> InlineKeyboardMarkup:
    models_map = {
        "sedan": ["BMW 5 / M5", "Zeekr 001", "Porsche 911 / Panamera", "Audi A6 / RS6", "Mercedes E / S-Class"],
        "crossover": ["BMW X5 / X6", "Geely Monjaro", "Porsche Cayenne", "Li Auto L7", "Mercedes GLE"],
        "large_suv": ["Li Auto L9", "Toyota LC 300", "Cadillac Escalade", "BMW X7", "Mercedes V-Class"]
    }
    models = models_map.get(car_class, [])
    buttons = []
    row = []
    for m in models:
        row.append(InlineKeyboardButton(text=m, callback_data=f"model:{car_class}:{m}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    
    buttons.append([InlineKeyboardButton(text="✏️ Ввести другую модель вручную", callback_data=f"model_manual:{car_class}")])
    buttons.append([InlineKeyboardButton(text="« Назад к выбору класса", callback_data="calc_start")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def services_keyboard(car_class: str, model_name: str) -> InlineKeyboardMarkup:
    buttons = []
    for s_code, s_data in SERVICES.items():
        buttons.append([InlineKeyboardButton(text=s_data["title"], callback_data=f"serv:{car_class}:{s_code}:{model_name}")])
    buttons.append([InlineKeyboardButton(text="« Назад к выбору авто", callback_data=f"class:{car_class}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def estimate_result_keyboard(car_class: str, s_code: str, model_name: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔥 Забронировать бокс + «Антидождь» в подарок",
                    callback_data=f"book_start:{car_class}:{s_code}:{model_name}"
                )
            ],
            [
                InlineKeyboardButton(text="📸 Посмотреть примеры работ", callback_data=f"portfolio:{s_code}"),
                InlineKeyboardButton(text="🔄 Рассчитать другую услугу", callback_data=f"model:{car_class}:{model_name}")
            ],
            [
                InlineKeyboardButton(text="« В главное меню", callback_data="to_main")
            ]
        ]
    )

def portfolio_categories_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛡 Оклейка в полиуретан (Глянец/Мат)", callback_data="port_view:risk_zones")],
            [InlineKeyboardButton(text="✨ Керамика и Восстановительная полировка", callback_data="port_view:ceramic")],
            [InlineKeyboardButton(text="🧼 Детейлинг салона и Кожа", callback_data="port_view:dry_clean")],
            [InlineKeyboardButton(text="« В главное меню", callback_data="to_main")]
        ]
    )

def b2b_pitch_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💬 Написать разработчику (@Nicky_pxl)", url=f"https://t.me/{DEV_CONTACT.replace('@', '')}")
            ],
            [
                InlineKeyboardButton(text="🤖 Аудит в основном боте студии", url=f"https://t.me/{DEV_BOT.replace('@', '')}?start=detailing_showcase")
            ],
            [
                InlineKeyboardButton(text="📢 Инженерный канал @pxlbot_studios", url=f"https://t.me/{DEV_CHANNEL.replace('@', '')}")
            ]
        ]
    )

def cancel_calc_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="❌ Отмена", callback_data="to_main")]]
    )
