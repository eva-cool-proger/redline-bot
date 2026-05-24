import logging
from aiogram import Router
from aiogram.types import ErrorEvent

router = Router()

@router.errors()
async def global_error_handler(event: ErrorEvent):
    """
    Глобальный обработчик ошибок. 
    Ловит любые исключения, чтобы бот не "падал" в консоли, 
    и сообщает пользователю, что что-то пошло не так.
    """
    logging.error(f"❌ Произошла ошибка: {event.exception}", exc_info=True)

    try:
        # Если ошибка произошла при нажатии на кнопку
        if event.update.callback_query:
            await event.update.callback_query.answer(
                "⚠️ Ошибка сети. Пожалуйста, подождите пару секунд и попробуйте снова.", 
                show_alert=True
            )
        # Если ошибка произошла при отправке обычного сообщения
        elif event.update.message:
            await event.update.message.answer(
                "⚠️ Произошла техническая ошибка (возможно, сбои сети). Попробуйте еще раз."
            )
    except Exception as e:
        # Если даже отправить сообщение об ошибке не получилось (например, вообще нет интернета)
        logging.error(f"Не удалось отправить уведомление об ошибке: {e}")