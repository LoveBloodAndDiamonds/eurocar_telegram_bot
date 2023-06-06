from aiogram import types


async def help_command(message: types.Message) -> None:
    """/help command"""
    with open("bot/templates/commands_text/help.txt", "r") as file:
        await message.answer(file.read())
