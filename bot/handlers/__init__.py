__all__ = ['register_user_handlers']

from aiogram import F
from aiogram import Router

from bot.handlers.faq_handlers import faq_message_handler, faq_callback_handler
from bot.handlers.rent_handlers import rent_message_handler, rent_callback_region, rent_callback_tariff, \
    rent_callback_car_class, rent_callback_car_model, confirm_order, handle_phone_number
from bot.models import KeyNames, FaqCallback, RentCallback
from bot.states import RentAutoState


def register_user_handlers(router: Router) -> None:
    """Register handlers."""
    router.message.register(faq_message_handler, F.text == KeyNames.FAQ_KEY)
    router.message.register(rent_message_handler, F.text == KeyNames.RENT_KEY)

    router.callback_query.register(faq_callback_handler, FaqCallback.filter())

    router.callback_query.register(rent_callback_region, RentCallback.filter(), RentAutoState.REGION)
    router.callback_query.register(rent_callback_tariff, RentCallback.filter(), RentAutoState.TARIFF)
    router.callback_query.register(rent_callback_car_class, RentCallback.filter(), RentAutoState.CAR_CLASS)
    router.callback_query.register(rent_callback_car_model, RentCallback.filter(), RentAutoState.CAR_MODEL)
    router.callback_query.register(confirm_order, RentCallback.filter(), RentAutoState.CONFIRM_ORDER)
    router.message.register(handle_phone_number, RentAutoState.PHONE_NUMBER)
