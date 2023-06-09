from aiogram import types

from bot.keyboards import get_main_keyboard, get_main_reply_markup


async def start_command(message: types.Message) -> None:
    """/start command"""
    with open("bot/templates/commands_text/start.txt", "r") as file:
        await message.answer(file.read().format(message.from_user.full_name),
                             reply_markup=get_main_keyboard())

    await message.answer("Воспользуйтесь клавиатурой для навигации:",
                         reply_markup=get_main_reply_markup())
