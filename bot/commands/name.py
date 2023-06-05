from aiogram import types
from aiogram.filters import CommandObject

from bot.redis_instance import redis


async def change_name_command(message: types.Message, command: CommandObject):
    if command.args:
        user_id = message.from_user.id
        command_arg = command.args
        await redis.set(f"{user_id}name", command_arg)
        await message.answer(f"Ваше имя было изменено на {command_arg}.")
    else:
        await message.answer("Чтобы изменить имя, необходимо ввести его после команды "
                             "/name.\nПример: /name Имя")
