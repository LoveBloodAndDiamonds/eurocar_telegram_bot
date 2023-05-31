from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup

from bot.models import KeyNames


def get_main_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=KeyNames.RENT_KEY)
    builder.button(text=KeyNames.FAQ_KEY)

    return builder.as_markup(resize_keyboard=True)
