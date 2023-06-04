import re

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram3_calendar import SimpleCalendar

from bot.keyboards import (
    get_rent_regions_keyboard,
    get_rent_car_classification_keyboard,
    get_car_models_keyboard,
    get_rent_tariffs_keyboard,
    get_accept_keyboard,
    get_phone_number_button,
)
from bot.models import CarClassification, RentCallback
from bot.redis_instance import redis
from bot.states import RentAutoState
from bot.utils import excel_data_updater_obj


async def rent_message_handler(message: types.Message, state: FSMContext) -> types.Message:
    """Handle FAQ message."""
    await state.clear()
    await state.set_state(RentAutoState.REGION)

    return await message.answer('Выберите дату:',
                                reply_markup=await SimpleCalendar().start_calendar())
    # return await message.answer('Я задам несколько вопросов, которые помогут подобрать автомобиль для Вас.\n\n'
    #                             '<b>Выберите Ваш регион:</b>',
    #                             reply_markup=get_rent_regions_keyboard())


async def process_simple_calendar(callback_query: types.CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'You selected {date.strftime("%d/%m/%Y")}'
        )


async def rent_callback_region(callback_query: types.CallbackQuery, callback_data: RentCallback, state: FSMContext):
    """Выбор региона."""
    if callback_data.answer_data == "cancel":  # Если пользователь нажал кнопку "Отмена"
        await state.clear()  # Очищаем состояние пользователя
        return await callback_query.message.delete()

    await state.update_data(REGION=callback_data.answer_data)
    await state.set_state(RentAutoState.TARIFF)
    state_data = await state.get_data()
    return callback_query.message.edit_text(
        f"Выбран регион '{state_data['REGION']}'.\n\n<b>Выберите тариф:</b>",
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
        f"Выбран тариф: '{state_data['TARIFF']}'\n\n<b>Выберите класс автомобиля:</b>\n\n{cars_class_description}",
        reply_markup=get_rent_car_classification_keyboard(region=state_data['REGION'],
                                                          tariff=state_data['TARIFF']))


async def rent_callback_car_class(callback_query: types.CallbackQuery, callback_data: RentCallback, state: FSMContext):
    """Выбор класса авто."""
    if callback_data.answer_data == "cancel":  # Если пользователь нажал кнопку "Отмена"
        await state.clear()  # Очищаем состояние пользователя
        return await callback_query.message.delete()

    if callback_data.answer_data == "back":  # Возвращаем пользователя на выбор тариф
        state_data = await state.get_data()
        await state.set_state(RentAutoState.TARIFF)
        return callback_query.message.edit_text(f"Выбран регион '{state_data['REGION']}'.\n\n<b>Выберите тариф:</b>",
                                                reply_markup=get_rent_tariffs_keyboard(region=state_data['REGION']))

    data: CarClassification.value = eval(f"{callback_data.answer_data}.value")  # Возможно, это колхозинг, но мне
    # показалось, что это достаточно удобный способ для получения классификации машин, которые входят
    # в классы вроде "Эконом", "Комфорт" и пр.

    await state.update_data(CAR_CLASS=(data[0], data[1]))
    await state.set_state(RentAutoState.CAR_MODEL)
    state_data = await state.get_data()
    car_models = excel_data_updater_obj.get_available_models(region=state_data["REGION"], car_class=data[0])
    return callback_query.message.edit_text(f"Выбран класс '{state_data['CAR_CLASS'][1]}'\n\n"
                                            f"<b>Выберите модель авто:</b>",
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
        return callback_query.message.edit_text(f"Выбран тариф '{state_data['TARIFF']}'\n\n"
                                                f"<b>Выберите класс автомобиля:</b>\n\n{cars_class_description}",
                                                reply_markup=get_rent_car_classification_keyboard(
                                                    region=state_data['REGION'],
                                                    tariff=state_data['TARIFF']))

    callback_data: tuple = eval(str(callback_data.answer_data))  # ('Nissan Qashqai', 'IGAR', 'AT')
    await state.update_data(CAR_MODEL=callback_data)
    await state.set_state(RentAutoState.CONFIRM_ORDER)
    state_data = await state.get_data()  # {'REGION': 'Москва',
    # 'TARIFF': 'Сутки (от 7 до 13 дней)',
    # 'CAR_CLASS': (['EGAR', 'IGAR', 'SFAR'], 'Кроссовер'),
    # 'CAR_MODEL': ('Nissan Qashqai', 'IGAR', 'AT')}
    # car_class: str, tariff: str,
    rent_price = int(excel_data_updater_obj.get_price_by_options(region=state_data['REGION'],
                                                                 car_class=state_data['CAR_MODEL'][1],
                                                                 tariff=state_data['TARIFF']))
    text = "<b>Подтвердите выбор:</b>\n\n" \
           f"Ваш регион: {state_data['REGION']}\n" \
           f"Выбранный тариф: {state_data['TARIFF']}\n" \
           f"Класс авто: {state_data['CAR_CLASS'][1]}\n" \
           f"Модель авто: {state_data['CAR_MODEL'][0]}\n" \
           f"Тип коробки передач: {state_data['CAR_MODEL'][2]}\n" \
           f"Стоимость аренды: <b>{rent_price}</b> руб.\n"
    return await callback_query.message.edit_text(text, reply_markup=get_accept_keyboard())


async def confirm_order(callback_query: types.CallbackQuery, callback_data: RentCallback, state: FSMContext):
    """Подтверждение заказа"""
    """Выбор модели авто."""
    if callback_data.answer_data == "cancel":  # Если пользователь нажал кнопку "Отмена"
        await state.clear()  # Очищаем состояние пользователя
        return await callback_query.message.delete()

    if callback_data.answer_data == "back":  # Возвращаем пользователя на выбор марки авто
        await state.set_state(RentAutoState.CAR_MODEL)
        state_data = await state.get_data()
        car_models = excel_data_updater_obj.get_available_models(region=state_data["REGION"],
                                                                 car_class=state_data["CAR_CLASS"][0])
        return callback_query.message.edit_text(f"Выбран класс '{state_data['CAR_CLASS'][1]}'\n\n"
                                                f"<b>Выберите модель авто:</b>",
                                                reply_markup=get_car_models_keyboard(
                                                    region=state_data['REGION'],
                                                    car_models=car_models,
                                                    tariff=state_data['TARIFF']))

    state_data = await state.get_data()
    rent_price = int(excel_data_updater_obj.get_price_by_options(region=state_data['REGION'],
                                                                 car_class=state_data['CAR_MODEL'][1],
                                                                 tariff=state_data['TARIFF']))
    await state.update_data(CONFIRM_ORDER=rent_price)
    await state.set_state(RentAutoState.PHONE_NUMBER)
    state_data = await state.get_data()
    phone_number = await redis.get(f'{callback_query.from_user.id}')
    phone_number = phone_number.decode('utf-8').strip() if phone_number else False
    reply_markup = get_phone_number_button(str(phone_number)) if phone_number else None  # Добавляем клавиатуру с
    # прошлым указанным номером, только если он есть

    return await callback_query.message.edit_text(text=f"Ваш регион: {state_data['REGION']}\n"
                                                       f"Выбранный тариф: {state_data['TARIFF']}\n"
                                                       f"Класс авто: {state_data['CAR_CLASS'][1]}\n"
                                                       f"Модель авто: {state_data['CAR_MODEL'][0]}\n"
                                                       f"Тип коробки передач: {state_data['CAR_MODEL'][2]}\n"
                                                       f"Стоимость аренды: <b>{rent_price}</b> руб.\n\n"
                                                       f"✅<b> Вы подтвердили заказ</b>\n"
                                                       f"В следующем сообщении <b>введите номер телефона</b> в формате "
                                                       f"<b>+7</b>, на который Вам перезвонит менеджер, для "
                                                       f"уточнения дальнейших инструкций: ",
                                                  reply_markup=reply_markup)


async def handle_phone_number(message: types.Message, state: FSMContext):
    """Ловим сообщение с номером телефона от юзера."""
    phone_nubmer = message.text
    phone_regex = re.compile(r'^\+7\d{10}$')
    if phone_regex.match(phone_nubmer):
        await redis.set(message.from_user.id, phone_nubmer)
        await state.update_data(PHONE_NUMBER=phone_nubmer)
        state_data = await state.get_data()
        await state.clear()
        print(state_data)  # todo send mail
        return await message.answer(f'Ваш номер телефона <code>{phone_nubmer}</code>, менеджер свяжется с Вами в '
                                    f'ближайшее время.')
    else:
        return await message.answer(f'Вы ввели неправильный номер телефона, попробуйте еще раз:')


async def handle_phone_number_callback(callback_query: types.CallbackQuery, state: FSMContext):
    """Ловим callback с номером телефона от юзера."""
    phone_nubmer = callback_query.data
    phone_regex = re.compile(r'^\+7\d{10}$')
    if phone_regex.match(phone_nubmer):
        await state.update_data(PHONE_NUMBER=phone_nubmer)
        state_data = await state.get_data()
        await state.clear()
        print(state_data)  # todo send mail
        await callback_query.message.edit_text(text=f"Ваш регион: {state_data['REGION']}\n"
                                                    f"Выбранный тариф: {state_data['TARIFF']}\n"
                                                    f"Класс авто: {state_data['CAR_CLASS'][1]}\n"
                                                    f"Модель авто: {state_data['CAR_MODEL'][0]}\n"
                                                    f"Тип коробки передач: {state_data['CAR_MODEL'][2]}\n"
                                                    f"Стоимость аренды: <b>{state_data['CONFIRM_ORDER']}</b> руб.\n\n"
                                                    f"✅<b> Вы подтвердили заказ</b>\n")
        return await callback_query.message.answer(f'Ваш номер телефона <code>{phone_nubmer}</code>,'
                                                   f' менеджер свяжется с Вами в ближайшее время.')
    else:
        return await callback_query.message.answer(f'Вы ввели неправильный номер телефона, попробуйте еще раз:')
