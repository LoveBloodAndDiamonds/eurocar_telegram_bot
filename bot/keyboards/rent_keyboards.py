from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, KeyboardButton

from bot.models import KeyNames, RentCallback, RentCallbackNames, CarClassification
from bot.utils import excel_data_updater_obj


def construct(builder: InlineKeyboardBuilder, adjust: int or bool = 1, resize_keyboard: bool = True,
              add_cancel_key: bool = True, add_back_key: bool = True) -> InlineKeyboardMarkup:
    """Remove some lines by this func."""
    if not (add_back_key and add_cancel_key):
        '''Если кнопки назад и закрыть не одновременно'''
        if add_back_key:  # Add cancel key
            builder.button(text=KeyNames.BACK_KEY,
                           callback_data=RentCallback(current_answer='None', answer_data='back'))
        if add_cancel_key:  # Add cancel key
            builder.button(text=KeyNames.CLOSE_KEY,
                           callback_data=RentCallback(current_answer='None', answer_data='cancel'))
        if adjust:
            builder.adjust(adjust)  # Make rows

    else:
        '''Если одновременно'''
        builder.button(text=KeyNames.BACK_KEY,  # Добавляем кнопку в новый ряд
                       callback_data=RentCallback(current_answer='None', answer_data='back'))
        if adjust:  # Выравниваем кнопки
            builder.adjust(adjust)  # Make rows
        builder.button(text=KeyNames.CLOSE_KEY,  # Добавляем кнопку в последний ряд
                       callback_data=RentCallback(current_answer='None', answer_data='cancel'))
    return builder.as_markup(resize_keyboard=resize_keyboard)


def get_rent_regions_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    # lst = [[i + j for j in range(1, 6)] for i in range(0, 26, 5)]
    # print(lst)
    # for range_list in lst:
    #     for r in range_list:
    #         builder.button(text=str(r), callback_data=str(r))
    #     builder.adjust(5)
    # return builder.as_markup()
    for region in excel_data_updater_obj.get_available_regions():  # todo
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
        prices_label = f"({min(prices)} - {max(prices)} руб.)" if min(prices) != max(prices) else f"({min(prices)} руб.)"
        builder.button(text=str(values[3]) + " " + str(values[1]) + " " + prices_label,
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
    for model in car_models:  # (car_model, spec, transmission,)
        price = int(excel_data_updater_obj.get_price_by_options(
            region=region,
            car_class=model[1],
            tariff=tariff
        ))
        builder.button(text=f"{model[0]} [{model[2]}] ({price} руб.)", callback_data=RentCallback(
            current_answer=RentCallbackNames.CAR_MODEL,
            answer_data=str(model)
        ))
    return construct(builder)


def get_accept_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=KeyNames.ACCEPT_KEY,  # Add key accept
                   callback_data=RentCallback(current_answer=RentCallbackNames.FINISH,
                                              answer_data='accept_order'))
    builder.button(text=KeyNames.BACK_KEY,  # Add back key
                   callback_data=RentCallback(current_answer='None', answer_data='back'))
    builder.adjust(1)
    builder.button(text=KeyNames.CLOSE_KEY,  # Add cancel key
                   callback_data=RentCallback(current_answer='None', answer_data='cancel'))
    return builder.as_markup()


def get_phone_number_button(phone_number: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=f"Использовать {phone_number}", callback_data=phone_number)
    return builder.as_markup()
