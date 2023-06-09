import re

from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.redis_instance import redis
from bot.utils import generate_preview_text, send_email
from bot.keyboards import get_main_reply_markup


async def phone_number_handler(message: types.Message, state: FSMContext):
    phone_regex = re.compile(r'^\+7\d{10}$')
    phone_regex_2 = re.compile(r'^7\d{10}$')
    phone_regex_3 = re.compile(r'^8\d{10}$')
    if phone_regex.match(message.text) or phone_regex_2.match(message.text) or phone_regex_3.match(message.text):
        await state.update_data(PHONE_NUMBER=message.text)
        await redis.set(f"{message.from_user.id}phone", message.text)
        state_data = await state.get_data()
        await state.clear()
        await send_email(data=state_data)

        return await message.answer(
            "✅<b> Вы подтвердили заказ!</b>\n"
            f"<b>{state_data['USER_REAL_NAME'].capitalize()}</b>, менеджер свяжется с Вами в ближайшее время "
            f"по телефону <code>{message.text}</code>.\n"
            f"Используйте клавиатуру, чтобы оформить новый заказ:",
            reply_markup=get_main_reply_markup())
    else:
        return await message.answer("Вы ввели неправильный номер телефона, номер телефона может быть в формате "
                                    "<code>+79</code>.")


async def phone_number_callback_handler(callback_querry: types.CallbackQuery, state: FSMContext):
    await state.update_data(PHONE_NUMBER=callback_querry.data)
    state_data = await state.get_data()
    prev_text = generate_preview_text(state_data)
    await state.clear()
    await send_email(data=state_data)

    await callback_querry.message.edit_text(text=prev_text + "✅<b> Вы подтвердили заказ</b>")
    return await callback_querry.message.answer(f"<b>{state_data['USER_REAL_NAME'].capitalize()}</b>, менеджер свяжется "
                                                f"с Вами в ближайшее время по телефону "
                                                f"<code>{callback_querry.data}</code>.\n"
                                                f"Используйте клавиатуру, чтобы оформить новый заказ:",
                                                reply_markup=get_main_reply_markup())
