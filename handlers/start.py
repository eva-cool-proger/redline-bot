from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery

from database.db import get_user_lang, add_user
from keyboards.inline import get_lang_keyboard, get_location_keyboard, get_start_virtual_keyboard
from utils.content import get_content

router = Router()

@router.message(Command("help"))
async def cmd_help(message: Message):
    user_lang = await get_user_lang(message.from_user.id) or "ru"
    
    texts = {
        "ru": "<b>Как пользоваться гидом:</b>\n\n1️⃣ Вы можете идти по городу и сканировать QR-коды.\n2️⃣ Нажимайте кнопки для виртуальной прогулки.\n\n/start — Перезапустить\n/lang — Сменить язык",
        "en": "<b>How to use the guide:</b>\n\n1️⃣ Scan QR codes on the street.\n2️⃣ Press buttons for a virtual walk.\n\n/start — Restart\n/lang — Change language",
        "zh": "<b>如何使用指南:</b>\n\n1️⃣ 扫描街上的二维码。\n2️⃣ 点击按钮进行虚拟漫步。\n\n/start — 重新开始\n/lang — 更改语言"
    }
    await message.answer(texts.get(user_lang, texts["ru"]), parse_mode="HTML")

@router.message(Command("lang", "language"))
async def cmd_lang(message: Message):
    await message.answer("Выберите язык / Choose your language / 请选择语言:", reply_markup=get_lang_keyboard("change"))

@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject):
    content = get_content()
    location_id = command.args 
    user_lang = await get_user_lang(message.from_user.id)
    if not location_id or location_id not in content:
        if not user_lang:
            await message.answer(
                "Добро пожаловать! Выберите язык / Choose your language / 请选择语言:", 
                reply_markup=get_lang_keyboard("empty_start")
            )
            return 
        texts = {
            "ru": "Вы находитесь в главном меню.\nИщите QR-коды на улице или начните маршрут прямо сейчас!",
            "en": "Welcome! Find QR codes on the street or start the route now!",
            "zh": "欢迎！在街上寻找二维码或立即开始路线！"
        }
        await message.answer(texts.get(user_lang, texts["ru"]), reply_markup=get_start_virtual_keyboard(user_lang))
        return
    if user_lang:
        await send_location_card(message, location_id, user_lang)
    else:
        await message.answer("Выберите язык / Choose your language / 请选择语言:", reply_markup=get_lang_keyboard(location_id))

@router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: CallbackQuery):
    _, lang, payload = callback.data.split("_", 2)
    
    await callback.answer()
    await add_user(callback.from_user.id, lang)
    await callback.message.edit_reply_markup(reply_markup=None)
    
    if payload == "change":
        texts = {"ru": "✅ Язык изменен!", "en": "✅ Language changed!", "zh": "✅ 语言已更改！"}
        await callback.message.answer(texts.get(lang, texts["ru"]))
    elif payload == "empty_start":
        texts = {"ru": "Отлично! Теперь вы можете начать маршрут.", "en": "Great! Now you can start.", "zh": "太棒了！现在您可以开始了。"}
        await callback.message.answer(texts.get(lang, texts["ru"]), reply_markup=get_start_virtual_keyboard(lang))
    else:
        await send_location_card(callback.message, payload, lang)
        
async def send_location_card(message: Message, loc_id: str, lang: str):
    content = get_content()
    data = content[loc_id][lang]
    
    kb = get_location_keyboard(loc_id, content[loc_id]["next_loc"], lang)
    text = f"<b>📍 {data['title']}</b>\n\n{data['desc']}"
    
    photo_url = content[loc_id].get("photo_loc")
    if not photo_url:
        photo_url = "https://placehold.co/800x500/EEEEEE/31343C/png?text=Location+Photo"
    
    if len(text) <= 1024:
        await message.answer_photo(photo=photo_url, caption=text, reply_markup=kb, parse_mode="HTML")
    else:
        await message.answer_photo(photo=photo_url)
        await message.answer(text=text, reply_markup=kb, parse_mode="HTML")