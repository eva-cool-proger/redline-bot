from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BUTTONS = {
    "ru": {
        "start_route": "🚩 Начать маршрут",
        "continue": "🚶‍♂️ Продолжить маршрут",
        "im_here": "✅ Я на месте",
        "map": "📍 На карте",
        "restart": "🔄 В начало"
    },
    "en": {
        "start_route": "🚩 Start route",
        "continue": "🚶‍♂️ Continue route",
        "im_here": "✅ I'm here",
        "map": "📍 On Map",
        "restart": "🔄 Restart"
    },
    "zh": {
        "start_route": "🚩 开始路线",
        "continue": "🚶‍♂️ 继续路线",
        "im_here": "✅ 我到了",
        "map": "📍 在地图上",
        "restart": "🔄 重新开始"
    }
}

def get_lang_keyboard(payload: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data=f"lang_ru_{payload}")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data=f"lang_en_{payload}")],
        [InlineKeyboardButton(text="🇨🇳 中文", callback_data=f"lang_zh_{payload}")]
    ])

def get_start_virtual_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=BUTTONS[lang]["start_route"], callback_data="arrive_loc_1")]
    ])

def get_location_keyboard(loc_id: str, next_loc: str, lang: str) -> InlineKeyboardMarkup:
    if next_loc == "end":
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=BUTTONS[lang]["restart"], callback_data="restart")]
        ])
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=BUTTONS[lang]["continue"], callback_data=f"nav_{loc_id}")]
    ])

def get_navigation_keyboard(next_loc: str, yandex_url: str, lang: str) -> InlineKeyboardMarkup:
    keys = []
    # Если URL в базе пустой, кнопка "На карте" просто не добавится
    if yandex_url:
        keys.append([InlineKeyboardButton(text=BUTTONS[lang]["map"], url=yandex_url)])
    
    keys.append([InlineKeyboardButton(text=BUTTONS[lang]["im_here"], callback_data=f"arrive_{next_loc}")])
    return InlineKeyboardMarkup(inline_keyboard=keys)