from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.keyboards import (
    get_rent_regions_keyboard,
    get_rent_car_classification_keyboard,
    get_car_models_keyboard,
    get_rent_tariffs_keyboard
)
from bot.models import CarClassification, RentCallback
from bot.states import RentAutoState
from bot.utils import excel_data_updater_obj


async def rent_message_handler(message: types.Message, state: FSMContext) -> types.Message:
    """Handle FAQ message."""
    await state.set_state(RentAutoState.REGION)
    return await message.answer('Я задам несколько вопросов, которые помогут подобрать автомобиль для Вас.\n\n'
                                '<b>Выберите Ваш регион:</b>',
                                reply_markup=get_rent_regions_keyboard())


async def rent_callback_region(callback_query: types.CallbackQuery, callback_data: RentCallback, state: FSMContext):
    """Выбор региона."""
    if callback_data.answer_data == "cancel":  # Если пользователь нажал кнопку "Отмена"
        await state.clear()  # Очищаем состояние пользователя
        return await callback_query.message.delete()

    await state.update_data(REGION=callback_data.answer_data)
    await state.set_state(RentAutoState.TARIFF)
    state_data = await state.get_data()
    return callback_query.message.edit_text(
        f"Отлично, теперь выберите тариф:",
        reply_markup=get_rent_tariffs_keyboard(region=state_data['REGION']))


async def rent_callback_tariff(callback_query: types.CallbackQuery, callback_data: RentCallback, state: FSMContext):
    """Выбор тарифа."""
    if callback_data.answer_data == "cancel":  # Если пользователь нажал кнопку "Отмена"
        await state.clear()  # Очищаем состояние пользователя
        return await callback_query.message.delete()

    if callback_data.answer_data == "back":  # Возвращаем пользователя на выбор региона
        await state.set_state(RentAutoState.REGION)
        return await callback_query.message.edit_text('Я задам несколько вопросов, которые помогут подобрать автомобиль'
                                                   ' для Вас.\n\n<b>Выберите Ваш регион:</b>',
                                                   reply_markup=get_rent_regions_keyboard())

    await state.update_data(TARIFF=callback_data.answer_data)
    await state.set_state(RentAutoState.CAR_CLASS)
    state_data = await state.get_data()

    cars_class_description = ""
    for classification in CarClassification:
        v = classification.value
        cars_class_description += f"<b>{v[3]} {v[1]}</b>: {v[2]}\n\n"
    return callback_query.message.edit_text(
        f"Отлично, теперь выберите класс автомобиля:\n\n{classification}",
        reply_markup=get_rent_car_classification_keyboard(region=state_data['REGION'],
                                                          tariff=state_data['TARIFF']))


async def rent_callback_car_class(callback_query: types.CallbackQuery, callback_data: RentCallback, state: FSMContext):
    """Выбор класса авто."""
    if callback_data.answer_data == "cancel":  # Если пользователь нажал кнопку "Отмена"
        await state.clear()  # Очищаем состояние пользователя
        return await callback_query.message.delete()

    if callback_data.answer_data == "back":  # Возвращаем пользователя на выбор тариффа
        state_data = await state.get_data()
        await state.set_state(RentAutoState.TARIFF)
        return callback_query.message.edit_text(f"Отлично, теперь выберите тариф:",
                                                reply_markup=get_rent_tariffs_keyboard(region=state_data['REGION']))

    data: CarClassification.value = eval(f"{callback_data.answer_data}.value")  # Возможно, это колхозинг, но мне
    # показалось, что это достаточно удобный способ для получения классификации машин, которые входят
    # в классы вроде "Эконом", "Комфорт" и пр.

    await state.update_data(CAR_CLASS=data)
    await state.set_state(RentAutoState.CAR_MODEL)
    state_data = await state.get_data()
    car_models = excel_data_updater_obj.get_available_models(region=state_data["REGION"], car_class=data[0])
    return callback_query.message.edit_text(f"Отлично, теперь выберите модель авто:",
                                            reply_markup=get_car_models_keyboard(
                                                region=state_data['REGION'],
                                                car_models=car_models,
                                                tariff=state_data['TARIFF']))


async def rent_callback_car_model(callback_query: types.CallbackQuery, callback_data: RentCallback, state: FSMContext):
    """Выбор модели авто."""
    if callback_data.answer_data == "cancel":  # Если пользователь нажал кнопку "Отмена"
        await state.clear()  # Очищаем состояние пользователя
        return await callback_query.message.delete()

    if callback_data.answer_data == "back":  # Возвращаем пользователя на выбор класса авто
        state_data = await state.get_data()
        await state.set_state(RentAutoState.CAR_CLASS)
        cars_class_description = ""
        for classification in CarClassification:
            v = classification.value
            cars_class_description += f"<b>{v[3]} {v[1]}</b>: {v[2]}\n\n"
        return callback_query.message.edit_text(
            f"Отлично, теперь выберите класс автомобиля:\n\n{classification}",
            reply_markup=get_rent_car_classification_keyboard(region=state_data['REGION'],
                                                              tariff=state_data['TARIFF']))

    callback_data: tuple = eval(str(callback_data.answer_data))  # ('Nissan Qashqai', 'IGAR', 'AT')
    await state.update_data(CAR_MODEL=callback_data)
    data = await state.get_data()  # {'REGION': 'Москва',
    # 'TARIFF': 'Сутки (от 7 до 13 дней)',
    # 'CAR_CLASS': (['EGAR', 'IGAR', 'SFAR'], 'Кроссовер', '#Текст про кроссовер', '🚙'),
    # 'CAR_MODEL': ('Nissan Qashqai', 'IGAR', 'AT')}
    text = "Подтвердите выбор:\n\n" \
           f"Ваш регион: {data['REGION']}\n" \
           f"Выбранный тариф: {data['TARIFF']}\n" \
           f"Класс авто: {data['CAR_CLASS'][1]}\n" \
           f"Модель авто: {data['CAR_MODEL'][0]}\n" \
           f"Тип коробки передач: {data['CAR_MODEL'][2]}\n"
    return await callback_query.message.edit_text(text)
