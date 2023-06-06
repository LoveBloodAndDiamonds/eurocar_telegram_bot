from aiogram import types

from bot.keyboards import get_faq_keyboard, get_back_key
from bot.models import FaqCallback


async def faq_message_handler(message: types.Message) -> types.Message:
    """Handle FAQ message."""
    return await message.answer('Выберите интересующий Вас вопрос:', reply_markup=get_faq_keyboard())


async def faq_callback_handler(callback_query: types.CallbackQuery, callback_data: FaqCallback
                               ) -> types.Message or bool:
    """Handle faq keyboard callbacks."""
    if callback_data.answer == 'back':
        return await callback_query.message.edit_text(text='Выберите интересующий Вас вопрос:',
                                                      reply_markup=get_faq_keyboard())
    if callback_data.answer == 'close':
        return await callback_query.message.delete()
    else:
        with open(f"bot/templates/faq/{callback_data.answer}.txt", "r") as file:
            return await callback_query.message.edit_text(text=file.read(), reply_markup=get_back_key())
