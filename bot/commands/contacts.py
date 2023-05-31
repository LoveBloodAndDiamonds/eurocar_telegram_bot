from aiogram import types


async def contacts_command(message: types.Message) -> types.Message:
    """/contacts command"""
    with open("templates/commands_text/contacts.txt", "r") as file:
        return await message.answer(file.read())
