__all__ = ['get_main_keyboard', 'get_faq_keyboard', 'get_back_key', "get_rent_regions_keyboard",
           "get_rent_car_classification_keyboard", "get_car_models_keyboard",
           "get_accept_keyboard", "get_phone_number_button", "get_main_reply_markup", "get_user_real_name_button"]

from bot.keyboards.faq_keyboards import get_faq_keyboard, get_back_key
from bot.keyboards.main_keyboard import get_main_keyboard, get_main_reply_markup
from bot.keyboards.rent_keyboards import (
    get_rent_regions_keyboard,
    get_rent_car_classification_keyboard,
    get_car_models_keyboard,
    get_accept_keyboard,
    get_phone_number_button,
    get_user_real_name_button
)
