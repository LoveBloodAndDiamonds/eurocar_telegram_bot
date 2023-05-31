from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup

from bot.models import CarClassification
from bot.models import KeyNames


def get_class_rent_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for classification in CarClassification.__members__.values():
        builder.add(InlineKeyboardButton(text=f"{classification.value[0]}",
                                         callback_data=f'rent_class_{classification.value[0]}'))
    return builder.as_markup(resize_keyboard=True)


def get_back_key() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=KeyNames.BACK_KEY, callback_data='faq_back')
    return builder.as_markup(resize_keyboard=True)
