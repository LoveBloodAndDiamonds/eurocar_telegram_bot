from aiogram import types

from bot.keyboards import get_faq_keyboard, get_back_key


async def faq_message_handler(message: types.Message) -> types.Message:
    return await message.answer('Выберите интересующий Вас вопрос:', reply_markup=get_faq_keyboard())


async def faq_callback_handler(callback_query: types.CallbackQuery) -> types.Message:
    data_postfix = callback_query.data.removeprefix('faq_')
    if data_postfix == 'back':
        return await callback_query.message.edit_text(text='Выберите интересующий Вас вопрос:',
                                                      reply_markup=get_faq_keyboard())
    else:
        with open(f"templates/faq/{data_postfix}.txt", "r") as file:
            return await callback_query.message.edit_text(text=file.read(), reply_markup=get_back_key())
