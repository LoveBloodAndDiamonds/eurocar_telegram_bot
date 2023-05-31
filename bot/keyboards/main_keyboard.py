from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup


def get_main_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text='Аренда 🚙')
    builder.button(text='FAQ ❔')

    return builder.as_markup(resize_keyboard=True)
