from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup

from bot.models import KeyNames, FaqCallback


def construct(builder: InlineKeyboardBuilder, adjust: int or bool = 1, resize_keyboard: bool = True)\
        -> InlineKeyboardMarkup:
    """Remove some lines by this func."""
    if adjust:
        builder.adjust(adjust)  # Make rows
    return builder.as_markup(resize_keyboard=resize_keyboard)


def get_faq_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    btns = [
        ('Какие бывают виды аренды?', FaqCallback(answer='rent_types'),),
        ('Какие документы нужны для аренды?', FaqCallback(answer='documents')),
        ('Могут ли мне отказать в аренде?', FaqCallback(answer='rent_decline')),
        ('Как работает страховка?', FaqCallback(answer='insurance')),
    ]
    for btn in btns:
        builder.button(text=btn[0], callback_data=btn[1])

    return construct(builder)


def get_back_key() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=KeyNames.BACK_KEY, callback_data=FaqCallback(answer='back'))
    return builder.as_markup(resize_keyboard=True)
