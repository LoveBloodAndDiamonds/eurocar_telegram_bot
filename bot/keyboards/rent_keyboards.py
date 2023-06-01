from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup

from bot.models import CarClassification
from bot.models import KeyNames
from bot.models import Regions
from bot.models import RentCallback


def construct(builder: InlineKeyboardBuilder, adjust: int or bool = 1, resize_keyboard: bool = True)\
        -> InlineKeyboardMarkup:
    """Remove some lines by this func."""
    if adjust:
        builder.adjust(adjust)  # Make rows
    return builder.as_markup(resize_keyboard=resize_keyboard)


def get_rent_regions_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for region in Regions.__members__.values():
        builder.button(text=f"{region.value[0]}",
                       callback_data=RentCallback(current_answer='region', answer_data=str(region.value[1])))
    return construct(builder)


def get_rent_class_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for classification in CarClassification.__members__.values():
        builder.add(InlineKeyboardButton(text=f"{classification.value[0]}",
                                         callback_data=f'rent_class_{classification.value[0]}'))
    return construct(builder)


def get_back_key() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=KeyNames.BACK_KEY, callback_data='faq_back')
    return builder.as_markup(resize_keyboard=True)
