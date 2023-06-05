from aiogram import types

from bot.keyboards import get_main_keyboard


async def unhandled_message(message: types.Message) -> types.Message:
    return await message.answer('Я Вас не понимаю, используйте клавиатуру для навигации.',
                                reply_markup=get_main_keyboard())


async def unhandled_querry(callback_querry: types.CallbackQuery):
    await callback_querry.answer('Данная клавиатура больше не работает.')
    return await callback_querry.message.delete()
