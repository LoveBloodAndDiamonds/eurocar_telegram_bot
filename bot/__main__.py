import asyncio
import logging
import os

from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
from dotenv import load_dotenv

from commands import register_user_commands, bot_commands
from handlers import register_user_handlers

load_dotenv()


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    dp = Dispatcher()
    bot = Bot(token=os.getenv('BOT_TOKEN'), parse_mode='HTML')

    commands_for_bot = []
    for cmd in bot_commands:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))
    await bot.set_my_commands(commands=commands_for_bot)

    register_user_commands(dp)
    register_user_handlers(dp)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info('Bot stopped')
