from aiogram import types

from bot.keyboards import get_main_keyboard


async def start_command(message: types.Message) -> None:
    """/start command"""
    with open("templates/commands_text/start.txt", "r") as file:
        await message.answer(file.read().format(message.from_user.full_name),
                             reply_markup=get_main_keyboard())
