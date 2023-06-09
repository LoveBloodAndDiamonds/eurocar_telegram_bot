from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from bot.models import KeyNames


def get_main_keyboard() -> ReplyKeyboardMarkup | None:
    builder = ReplyKeyboardBuilder()
    builder.button(text=KeyNames.RENT_KEY)
    builder.button(text=KeyNames.FAQ_KEY)

    return builder.as_markup(resize_keyboard=True)


def get_main_reply_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=KeyNames.RENT_KEY, callback_data="start_rent")
    builder.button(text=KeyNames.FAQ_KEY, callback_data="start_faq")
    builder.adjust(2)
    return builder.as_markup()
