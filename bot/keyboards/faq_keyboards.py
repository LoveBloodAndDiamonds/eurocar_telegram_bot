from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup

from bot.models import KeyNames


def get_faq_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for btn in [InlineKeyboardButton(text='Какие бывают виды аренды?', callback_data='faq_rent_types'),
                InlineKeyboardButton(text='Какие документы нужны для аренды?', callback_data='faq_documents'),
                InlineKeyboardButton(text='Могут ли мне отказать в аренде?', callback_data='faq_rent_decline'),
                InlineKeyboardButton(text='Как работает страховка?', callback_data='faq_insurance')]:
        builder.row(btn)

    return builder.as_markup(resize_keyboard=True)


def get_back_key() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=KeyNames.BACK_KEY, callback_data='faq_back')
    return builder.as_markup(resize_keyboard=True)
