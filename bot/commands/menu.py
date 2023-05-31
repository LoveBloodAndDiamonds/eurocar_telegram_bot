from aiogram import types

from bot.keyboards import get_main_keyboard


async def show_menu_command(message: types.Message) -> None:
    """/menu command"""
    await message.answer(text='Меню обновлено.', reply_markup=get_main_keyboard())
