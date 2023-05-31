__all__ = ['register_user_commands', 'bot_commands']

from aiogram import Router
from aiogram.filters import CommandStart, Command

from bot.commands.contacts import contacts_command
from bot.commands.help import help_command
from bot.commands.menu import show_menu_command
from bot.commands.start import start_command

bot_commands = (
    ("help", "Помощь и справка"),
    ("contacts", "Показать контакты"),
    ("show_menu", "Показать меню")
)


def register_user_commands(router: Router) -> None:
    """Register commands"""
    router.message.register(start_command, CommandStart())
    router.message.register(help_command, Command(commands='help'))
    router.message.register(contacts_command, Command(commands='contacts'))
    router.message.register(show_menu_command, Command(commands='show_menu'))

