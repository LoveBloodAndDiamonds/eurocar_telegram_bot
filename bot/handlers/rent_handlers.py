from datetime import datetime

from aiogram import types
from aiogram.fsm.context import FSMContext

from aiogram3_calendar import SimpleCalendar
from bot.keyboards import (
    get_rent_regions_keyboard,
    get_rent_car_classification_keyboard,
    get_car_models_keyboard,
    get_accept_keyboard,
    get_phone_number_button,
    get_user_real_name_button
)
from bot.models import CarClassification, RentCallback, TextNames as Tn
from bot.redis_instance import redis
from bot.states import RentAutoState
from bot.utils import excel_data_updater_obj, generate_preview_text


async def rent_message_handler(message: types.Message or types.CallbackQuery, state: FSMContext) -> types.Message:
    """Handle FAQ message."""
    if isinstance(message, types.CallbackQuery):
        message = message.message

    await state.clear()  # Очищаем состояние, чтобы пользователь не запутался
    await state.set_state(RentAutoState.REGION)
    return await message.answer(f'Я задам Вам несколько вопросов, чтобы помочь оформить '
                                f'заявку на аренду автомобиля.\n\n'
                                '<b>Выберите Ваш регион:</b>',
                                reply_markup=get_rent_regions_keyboard())


async def rent_callback_region(callback_query: types.CallbackQuery, callback_data: RentCallback, state: FSMContext):
    """Выбор региона."""
    if callback_data.answer_data == "cancel":  # Если пользователь нажал кнопку "Отмена"
        await state.clear()  # Очищаем состояние пользователя
        return await callback_query.message.delete()

    await state.update_data(REGION=callback_data.answer_data)
    await state.set_state(RentAutoState.START_DATE)
    state_data = await state.get_data()

    return callback_query.message.edit_text(f"{generate_preview_text(state_data)}"
                                            f"<b>Выберите желаемую дату начала аренды:</b>",
                                            reply_markup=await SimpleCalendar().start_calendar())


async def get_start_date_from_calendar(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        date_now = datetime.now()
        date_now = date_now.replace(day=date_now.day - 1, hour=0, minute=0, second=0)
        if date >= date_now:
            date = date.date().isoformat()
            await state.update_data(START_DATE=date)
            await state.set_state(RentAutoState.END_DATE)
            state_data = await state.get_data()

            return callback_query.message.edit_text(f"{generate_preview_text(state_data)}"
                                                    f"<b>Выберите желаемую дату окончания аренды:</b>",
                                                    reply_markup=await SimpleCalendar().start_calendar())
        else:
            state_data = await state.get_data()
            return callback_query.message.edit_text(f"{generate_preview_text(state_data)}"
                                                    f"❗️Дата начала аренды не может быть раньше, чем сегодня.\n\n"
                                                    f"<b>Введите корректную дату начала аренды:</b>",
                                                    reply_markup=await SimpleCalendar().start_calendar())


async def start_date_calendar_back_or_close(callback_query: types.CallbackQuery, callback_data: RentCallback,
                                            state: FSMContext):
    if callback_data.answer_data == "cancel":  # Если пользователь нажал кнопку "Отмена"
        await state.clear()  # Очищаем состояние пользователя
        return await callback_query.message.delete()

    elif callback_data.answer_data == "back":  # Возвращаем пользователя на выбор региона
        await state.set_state(RentAutoState.REGION)
        return await callback_query.message.edit_text('<b>Выберите Ваш регион:</b>',
                                                      reply_markup=get_rent_regions_keyboard())


async def get_end_date_from_calendar(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        state_data = await state.get_data()
        start_date = datetime.strptime(state_data["START_DATE"], '%Y-%m-%d')
        if date >= start_date:
            date = date.date().isoformat()
            await state.update_data(END_DATE=date)
            await state.set_state(RentAutoState.CAR_CLASS)
            state_data = await state.get_data()

            # Вычисляем количество дней аренды авто
            start_date = datetime.fromisoformat(state_data["START_DATE"])
            end_date = datetime.fromisoformat(state_data["END_DATE"])
            days_delta = (end_date - start_date).days
            days_delta = 1 if not days_delta else days_delta  # if start date == end date
            await state.update_data(RENT_DAYS=days_delta)

            state_data["RENT_DAYS"] = days_delta

            return callback_query.message.edit_text(
                f"{generate_preview_text(state_data)}"
                f"<b>Выберите класс автомобиля:</b>\n\n"
                f"<i>В скобках указана предположительная стоимость аренды за выбранный Вами период аренды.</i>",
                reply_markup=get_rent_car_classification_keyboard(region=state_data['REGION'],
                                                                  tariff=days_delta))
        else:
            return callback_query.message.edit_text(
                f"{generate_preview_text(state_data)}"
                f"❗️Дата начала аренды не может быть раньше, чем дата начала аренды.\n\n"
                f"<b>Введите корректную дату окончания аренды:</b>",
                reply_markup=await SimpleCalendar().start_calendar())


async def end_date_calendar_back_or_close(callback_query: types.CallbackQuery, callback_data: RentCallback,
                                          state: FSMContext):
    if callback_data.answer_data == "cancel":  # Если пользователь нажал кнопку "Отмена"
        await state.clear()  # Очищаем состояние пользователя
        return await callback_query.message.delete()

    if callback_data.answer_data == "back":  # Возвращаем пользователя на выбор начальной даты
        state_data = await state.get_data()
        for key in ["RENT_DAYS", "START_DATE", "END_DATE", "CAR_CLASS", "CAR_MODEL", "CONFIRM_ORDER", "PHONE_NUMBER"]:
            state_data.pop(key, None)
        await state.clear()
        await state.update_data(**state_data)
        await state.set_state(RentAutoState.START_DATE)
        prev_text = generate_preview_text(state_data)
        return callback_query.message.edit_text(f"{prev_text}"
                                                f"<b>Выберите желаемую дату начала аренды:</b>",
                                                reply_markup=await SimpleCalendar().start_calendar())


async def rent_callback_car_class(callback_query: types.CallbackQuery, callback_data: RentCallback, state: FSMContext):
    """Выбор класса авто."""
    if callback_data.answer_data == "cancel":  # Если пользователь нажал кнопку "Отмена"
        await state.clear()  # Очищаем состояние пользователя
        return await callback_query.message.delete()

    if callback_data.answer_data == "back":  # Возвращаем пользователя на выбор даты окончания аренды
        state_data = await state.get_data()
        for key in ["RENT_DAYS", "END_DATE", "CAR_CLASS", "CAR_MODEL", "CONFIRM_ORDER", "PHONE_NUMBER"]:
            state_data.pop(key, None)
        await state.clear()
        await state.update_data(**state_data)
        await state.set_state(RentAutoState.END_DATE)
        prev_text = generate_preview_text(state_data)
        return callback_query.message.edit_text(f"{prev_text}"
                                                f"<b>Выберите желаемую дату окончания аренды:</b>",
                                                reply_markup=await SimpleCalendar().start_calendar())

    data: CarClassification.value = eval(f"{callback_data.answer_data}.value")  # Возможно, это колхозинг, но мне
    # показалось, что это достаточно удобный способ для получения классификации машин, которые входят
    # в классы вроде "Эконом", "Комфорт" и пр.

    await state.update_data(CAR_CLASS=(data[0], data[1]))
    await state.set_state(RentAutoState.CAR_MODEL)
    state_data = await state.get_data()

    car_models = excel_data_updater_obj.get_available_models(region=state_data["REGION"], car_class=data[0])
    return callback_query.message.edit_text(f"{generate_preview_text(state_data)}"
                                            f"<b>Выберите модель авто:</b>\n\n"
                                            f"<i>В скобках указана предположительная стоимость аренды за "
                                            f"выбранный Вами период аренды.</i>",
                                            reply_markup=get_car_models_keyboard(
                                                region=state_data['REGION'],
                                                car_models=car_models,
                                                tariff=state_data['RENT_DAYS']))


async def rent_callback_car_model(callback_query: types.CallbackQuery, callback_data: RentCallback, state: FSMContext):
    """Выбор модели авто."""
    if callback_data.answer_data == "cancel":  # Если пользователь нажал кнопку "Отмена"
        await state.clear()  # Очищаем состояние пользователя
        return await callback_query.message.delete()

    if callback_data.answer_data == "back":  # Возвращаем пользователя на выбор класса авто
        state_data = await state.get_data()
        for key in ["CAR_CLASS", "CAR_MODEL", "CONFIRM_ORDER", "PHONE_NUMBER"]:
            state_data.pop(key, None)
        await state.clear()
        await state.update_data(**state_data)
        await state.set_state(RentAutoState.CAR_CLASS)
        prev_text = generate_preview_text(state_data)
        return callback_query.message.edit_text(f"{prev_text}"
                                                f"<b>Выберите класс автомобиля:</b>",
                                                reply_markup=get_rent_car_classification_keyboard(
                                                    region=state_data['REGION'],
                                                    tariff=state_data['RENT_DAYS']))

    callback_data: tuple = eval(str(callback_data.answer_data))  # ('Nissan Qashqai', 'IGAR', 'AT')
    await state.update_data(CAR_MODEL=callback_data)
    await state.set_state(RentAutoState.RENT_PRICE)
    state_data = await state.get_data()
    rent_price = int(excel_data_updater_obj.get_price_by_options(region=state_data['REGION'],
                                                                 car_class=state_data['CAR_MODEL'][1],
                                                                 tariff=state_data['RENT_DAYS']))
    prev_text = generate_preview_text(state_data, additional_text=f"{Tn.T.format(int(rent_price))}")

    return await callback_query.message.edit_text(f"<b>Подтвердите выбор:</b>\n\n{prev_text}",
                                                  reply_markup=get_accept_keyboard())


async def confirm_order(callback_query: types.CallbackQuery, callback_data: RentCallback, state: FSMContext):
    """Подтверждение заказа"""
    """Выбор модели авто."""
    if callback_data.answer_data == "cancel":  # Если пользователь нажал кнопку "Отмена"
        await state.clear()  # Очищаем состояние пользователя
        return await callback_query.message.delete()

    if callback_data.answer_data == "back":  # Возвращаем пользователя на выбор марки авто
        state_data = await state.get_data()
        car_models = excel_data_updater_obj.get_available_models(region=state_data["REGION"],
                                                                 car_class=state_data["CAR_CLASS"][0])
        for key in ["CAR_MODEL", "CONFIRM_ORDER", "PHONE_NUMBER"]:
            state_data.pop(key, None)
        await state.clear()
        await state.update_data(**state_data)
        await state.set_state(RentAutoState.CAR_MODEL)
        prev_text = generate_preview_text(state_data)
        return callback_query.message.edit_text(f"{prev_text}"
                                                f"<b>Выберите модель авто:</b>",
                                                reply_markup=get_car_models_keyboard(
                                                    region=state_data['REGION'],
                                                    car_models=car_models,
                                                    tariff=state_data['RENT_DAYS']))

    state_data = await state.get_data()
    rent_price = int(excel_data_updater_obj.get_price_by_options(region=state_data['REGION'],
                                                                 car_class=state_data['CAR_MODEL'][1],
                                                                 tariff=state_data['RENT_DAYS']))
    await state.update_data(RENT_PRICE=rent_price)
    await state.set_state(RentAutoState.USER_REAL_NAME)

    user_name = await redis.get(f"{callback_query.from_user.id}name")
    user_name = user_name.decode('utf-8').strip()
    reply_markup = get_user_real_name_button(str(user_name)) if user_name else None  # Добавляем клавиатуру с
    # прошлым указанным именем, если оно есть

    prev_text = generate_preview_text(state_data, additional_text=f"{Tn.T.format(rent_price)}")

    return await callback_query.message.edit_text(text=f"{prev_text}"
                                                       f"✅<b> Вы подтвердили заказ</b>\n"
                                                       f"В следующем сообщении <b>введите Ваше имя</b>:",
                                                  reply_markup=reply_markup)
