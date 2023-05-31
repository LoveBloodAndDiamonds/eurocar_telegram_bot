__all__ = ['register_user_handlers']

from aiogram import F
from aiogram import Router

from bot.handlers.faq_handlers import faq_message_handler, faq_callback_handler
from bot.handlers.rent_handlers import rent_message_handler, rent_callback_handler
from bot.models import KeyNames


def register_user_handlers(router: Router) -> None:
    """Register handlers."""
    router.message.register(faq_message_handler, F.text == KeyNames.FAQ_KEY)
    router.message.register(rent_message_handler, F.text == KeyNames.RENT_KEY)
    router.callback_query.register(faq_callback_handler, F.data.startswith("faq_"))
    router.callback_query.register(rent_callback_handler, F.data.startswith("rent_class_"))
