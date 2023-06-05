import re

from aiogram import types
from aiogram.filters import CommandObject

from bot.redis_instance import redis


async def change_phone_command(message: types.Message, command: CommandObject):
    if command.args:
        phone_number = command.args
        phone_regex = re.compile(r'^\+7\d{10}$')
        phone_regex_2 = re.compile(r'^7\d{10}$')
        phone_regex_3 = re.compile(r'^8\d{10}$')
        if phone_regex.match(phone_number) or phone_regex_2.match(phone_number) or phone_regex_3.match(phone_number):
            await redis.set(f"{message.from_user.id}phone", phone_number)
            await message.answer(f"Вы поменяли номер телефона на <code>{phone_number}</code>.")
        else:
            await message.answer(f"Вы ввели неправильный номер телефона.\n"
                                 f"Введите его в формате +79XXXXXXXXX после команды /phone")
    else:
        await message.answer("Чтобы изменить номер телефона, необходимо ввести его после команды "
                             "/phone\nПример: /phone +791234567890")
