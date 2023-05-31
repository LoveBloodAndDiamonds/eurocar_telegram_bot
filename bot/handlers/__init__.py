__all__ = ['register_user_handlers']

from aiogram import Router
from aiogram import F

from bot.handlers.faq_handlers import faq_message_handler, faq_callback_handler


def register_user_handlers(router: Router) -> None:
    """Register handlers"""
    router.message.register(faq_message_handler, F.text == 'FAQ ❔')
    router.callback_query.register(faq_callback_handler, F.data.startswith("faq_"))



