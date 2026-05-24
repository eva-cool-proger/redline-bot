import contextlib
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from database.db import get_user_lang
from keyboards.inline import get_navigation_keyboard
from handlers.start import send_location_card
from utils.content import get_content

router = Router()

@router.callback_query(F.data.startswith("nav_"))
async def show_navigation(callback: CallbackQuery):
    await callback.answer()

    loc_id = callback.data.replace("nav_", "")
    user_lang = await get_user_lang(callback.from_user.id) or "ru"
    content = get_content()
    
    data = content[loc_id][user_lang]
    next_loc = content[loc_id]["next_loc"]
    
    # Безопасное получение yandex_url
    yandex_url = data.get("yandex_url", "")
    kb = get_navigation_keyboard(next_loc, yandex_url, user_lang)
    
    titles = {
        "ru": "🗺 <b>Как пройти:</b>\n\n",
        "en": "🗺 <b>Navigation:</b>\n\n",
        "zh": "🗺 <b>导航:</b>\n\n"
    }
    title = titles.get(user_lang, titles["ru"])
    text = f"{title}{data.get('nav_text', '')}"
    
    # Плейсхолдер для фото навигации, если оно отсутствует
    photo_url = content[loc_id].get("photo_nav")
    if not photo_url:
        photo_url = "https://placehold.co/800x500/EEEEEE/31343C/png?text=Navigation+Map"
    
    # Гасим только конкретную ошибку TelegramBadRequest
    with contextlib.suppress(TelegramBadRequest, Exception):
        await callback.message.edit_reply_markup(reply_markup=None)

    # Защита от лимитов Telegram (на всякий случай, если текст навигации тоже окажется длинным)
    if len(text) <= 1024:
        await callback.message.answer_photo(photo=photo_url, caption=text, reply_markup=kb, parse_mode="HTML")
    else:
        await callback.message.answer_photo(photo=photo_url)
        await callback.message.answer(text=text, reply_markup=kb, parse_mode="HTML")
    

@router.callback_query(F.data.startswith("arrive_"))
async def arrive_at_location(callback: CallbackQuery):
    await callback.answer()

    next_loc_id = callback.data.replace("arrive_", "")
    user_lang = await get_user_lang(callback.from_user.id) or "ru"
    
    with contextlib.suppress(TelegramBadRequest, Exception):
        await callback.message.edit_reply_markup(reply_markup=None)
        
    await send_location_card(callback.message, next_loc_id, user_lang)


@router.callback_query(F.data == "restart")
async def restart_route(callback: CallbackQuery):
    await callback.answer()

    user_lang = await get_user_lang(callback.from_user.id) or "ru"
    
    with contextlib.suppress(TelegramBadRequest, Exception):
        await callback.message.edit_reply_markup(reply_markup=None)
        
    await send_location_card(callback.message, "loc_1", user_lang)