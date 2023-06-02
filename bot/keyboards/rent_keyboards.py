from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup

from bot.models import KeyNames, RentCallback, RentCallbackNames, CarClassification
from bot.utils import excel_data_updater_obj


def construct(builder: InlineKeyboardBuilder, adjust: int or bool = 1, resize_keyboard: bool = True,
              add_cancel_key: bool = True) -> InlineKeyboardMarkup:
    """Remove some lines by this func."""
    if add_cancel_key:  # Add cancel key
        builder.button(text=KeyNames.CANCEL_KEY,
                       callback_data=RentCallback(current_answer='None', answer_data='cancel'))
    if adjust:
        builder.adjust(adjust)  # Make rows
    return builder.as_markup(resize_keyboard=resize_keyboard)


def get_rent_regions_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for region in excel_data_updater_obj.get_available_regions():
        builder.button(text=str(region),
                       callback_data=RentCallback(current_answer=RentCallbackNames.REGION, answer_data=str(region)))
    return construct(builder)


def get_rent_car_classification_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for classification in CarClassification:
        values = classification.value
        builder.button(text=str(values[3]) + " " + str(values[1]),
                       callback_data=RentCallback(current_answer=RentCallbackNames.CAR_CLASS,
                       answer_data=str(classification)))
    return construct(builder)
