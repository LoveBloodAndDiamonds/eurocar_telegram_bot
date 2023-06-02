import logging

from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.keyboards import get_rent_regions_keyboard, get_rent_car_classification_keyboard
from bot.models import CarClassification, RentCallback, KeyNames, RentCallbackNames
from bot.states import RentAutoState


async def rent_message_handler(message: types.Message, state: FSMContext) -> types.Message:
    """Handle FAQ message."""
    await state.set_state(RentAutoState.REGION)
    return await message.answer('Я задам несколько вопросов, которые помогут подобрать автомобиль для Вас.\n\n'
                                '<b>Выберите Ваш регион:</b>',
                                reply_markup=get_rent_regions_keyboard())


async def rent_callback_handler(callback_query: types.CallbackQuery, callback_data: RentCallback,
                                state: FSMContext) -> bool or types.Message:
    """Handle faq keyboard callbacks."""
    if callback_data.answer_data == "cancel":  # Если пользователь нажал кнопку "Отмена"
        await state.clear()  # Очищаем состояние пользователя
        return await callback_query.message.delete()

    elif callback_data.current_answer == RentCallbackNames.REGION:  # Выбор региона
        await state.update_data(REGION=callback_data.answer_data)
        await state.set_state(RentAutoState.CAR_CLASS)
        state_data = await state.get_data()
        return callback_query.message.edit_text(f"Отлично, Ваш регион {state_data}, теперь выберите тип авто:",
                                                reply_markup=get_rent_car_classification_keyboard())

    elif callback_data.current_answer == RentCallbackNames.CAR_CLASS:  # Выбор класса авто
        data: CarClassification.value = eval(f"{callback_data.answer_data}.value")  # Возможно, это колхозинг, но мне
        # показалось, что это достаточно удобный способ для получения классификации машин, которые входят
        # в классы вроде "Эконом", "Комфорт" и пр.
        print(data)
        await state.update_data(CAR_CLASS=callback_data)
        await state.set_state(RentAutoState.CAR_MODEL)
        state_data = await state.get_data()
        return callback_query.message.edit_text(f"Отлично, Вы выбрали класс авто {state_data}, теперь выберите модель"
                                                f"авто")

    return await callback_query.message.edit_text(f"Выберите Ваш регион или нажмите {KeyNames.CANCEL_KEY}",
                                                  reply_markup=get_rent_regions_keyboard())
