import logging

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup

from bot.models import KeyNames, RentCallback, RentCallbackNames, CarClassification
from bot.utils import excel_data_updater_obj


def construct(builder: InlineKeyboardBuilder, adjust: int or bool = 1, resize_keyboard: bool = True,
              add_cancel_key: bool = True, add_back_key: bool = True) -> InlineKeyboardMarkup:
    """Remove some lines by this func."""
    if add_back_key:  # Add cancel key
        builder.button(text=KeyNames.BACK_KEY,
                       callback_data=RentCallback(current_answer='None', answer_data='back'))
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
    return construct(builder, add_back_key=False)


def get_rent_car_classification_keyboard(region: str, tariff: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for classification in CarClassification:
        values = classification.value
        prices = [int(excel_data_updater_obj.get_price_by_options(
            region=region,
            car_class=car_class,
            tariff=tariff
        )) for car_class in values[0]]
        builder.button(text=str(values[3]) + " " + str(values[1]) + f" ({min(prices)} - {max(prices)})",
                       callback_data=RentCallback(current_answer=RentCallbackNames.CAR_CLASS,
                       answer_data=str(classification)))
    return construct(builder)


def get_rent_tariffs_keyboard(region: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    available_tariffs = excel_data_updater_obj.get_available_tariffs(region=region)
    for tariff in available_tariffs:
        builder.button(text=str(tariff),
                       callback_data=RentCallback(current_answer=RentCallbackNames.TARIFF,
                       answer_data=str(tariff)))
    return construct(builder)


def get_car_models_keyboard(region: str, car_models: list, tariff: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    # (car_model, spec, transmission,)
    for model in car_models:
        price = int(excel_data_updater_obj.get_price_by_options(
            region=region,
            car_class=model[1],
            tariff=tariff
        ))
        builder.button(text=f"{model[0]} [{model[2]}] ({price})", callback_data=RentCallback(
            current_answer=RentCallbackNames.CAR_MODEL,
            answer_data=str(model)
        ))
    return construct(builder)
