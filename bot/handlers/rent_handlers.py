from aiogram import types

from bot.keyboards import get_rent_regions_keyboard
from bot.models import CarClassification, RentCallback


async def rent_message_handler(message: types.Message) -> types.Message:
    """Handle FAQ message."""
    # text_with_classification = str()
    # for classification in CarClassification.__members__.values():
    #     text_with_classification += f'{classification.value[2]} ' \
    #                                 f'<b>{classification.value[0]}</b>: ' \
    #                                 f'{classification.value[1]}\n\n'

    return await message.answer('Я задам Вам несколько вопросов, которые помогут подобрать Вам автомобиль.\n\n'
                                '<b>Выберите Ваш регион:</b>',
                                reply_markup=get_rent_regions_keyboard())


async def rent_callback_handler(callback_query: types.CallbackQuery, callback_data: RentCallback) -> types.Message:
    """Handle faq keyboard callbacks."""
    print(callback_data)
    print(callback_data.current_answer)
    print(callback_data.answer_data)
    return await callback_query.message.answer(callback_data.answer_data)
