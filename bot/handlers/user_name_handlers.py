from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.keyboards import get_phone_number_button
from bot.redis_instance import redis
from bot.states import RentAutoState
from bot.utils import generate_preview_text


async def user_name_handler(message: types.Message, state: FSMContext):
    await state.update_data(USER_REAL_NAME=message.text)
    await redis.set(f"{message.from_user.id}name", message.text)
    state_data = await state.get_data()
    await state.set_state(RentAutoState.PHONE_NUMBER)

    phone_number = await redis.get(f"{message.from_user.id}phone")
    phone_number = phone_number.decode('utf-8').strip() if phone_number else None
    keyboard = get_phone_number_button(phone_number) if phone_number else None

    return await message.answer(f"<b>{state_data['USER_REAL_NAME']}</b>, в следующем сообщении "
                                f"отправьте Ваш номер телефона в формате <code>+79123456789</code>:",
                                reply_markup=keyboard)


async def user_name_callback_handler(callback_querry: types.CallbackQuery, state: FSMContext):
    await state.update_data(USER_REAL_NAME=callback_querry.data)
    state_data = await state.get_data()
    prev_text = generate_preview_text(state_data)
    await state.set_state(RentAutoState.PHONE_NUMBER)

    phone_number = await redis.get(f"{callback_querry.from_user.id}phone")
    phone_number = phone_number.decode('utf-8').strip() if phone_number else None
    keyboard = get_phone_number_button(phone_number) if phone_number else None

    return await callback_querry.message.edit_text(prev_text +
                                                   f"<b>{state_data['USER_REAL_NAME']}</b>, в следующем сообщении "
                                                   f"отправьте Ваш номер телефона в формате <code>+79123456789</code>:",
                                                   reply_markup=keyboard)
