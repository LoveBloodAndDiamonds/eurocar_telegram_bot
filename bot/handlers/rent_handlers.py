from aiogram import types

from bot.keyboards import get_class_rent_keyboard
from bot.models import CarClassification


async def rent_message_handler(message: types.Message) -> types.Message:
    """Handle FAQ message."""
    text_with_classification = str()
    for classification in CarClassification.__members__.values():
        text_with_classification += f'{classification.value[2]} ' \
                                    f'<b>{classification.value[0]}</b>: ' \
                                    f'{classification.value[1]}\n\n'

    return await message.answer('Я задам Вам несколько вопросов, которые помогут подобрать Вам автомобиль.\n\n'
                                f'{text_with_classification}'
                                '<b>Выберите класс автомобилей, который подходит Вам больше всего:</b>',
                                reply_markup=get_class_rent_keyboard())


async def rent_callback_handler(callback_query: types.CallbackQuery) -> types.Message:
    """Handle faq keyboard callbacks."""
    data_postfix = callback_query.data.removeprefix('rent_class_')
    return await callback_query.message.answer(data_postfix)
