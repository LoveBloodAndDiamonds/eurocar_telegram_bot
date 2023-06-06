import asyncio
import logging
import os

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand
from dotenv import load_dotenv

from bot.redis_instance import redis
from bot.commands import register_user_commands, bot_commands
from bot.handlers import register_user_handlers
from bot.utils import data_updater_th

load_dotenv()


async def set_up_commands(bot: Bot) -> None:
    """Set up commands what user will see."""
    commands_for_bot = []
    for cmd in bot_commands:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))
    await bot.set_my_commands(commands=commands_for_bot)


async def main() -> None:
    data_updater_th.start()  # Start to update data from excel table

    dp = Dispatcher(storage=RedisStorage(redis=redis))
    bot = Bot(token=os.getenv('BOT_TOKEN'), parse_mode='HTML')

    await set_up_commands(bot)

    register_user_commands(dp)
    register_user_handlers(dp)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.DEBUG)
        logging.info('Bot launched!')
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info('Bot stopped')
