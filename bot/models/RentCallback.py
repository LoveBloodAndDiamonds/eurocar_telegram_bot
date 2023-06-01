from aiogram.filters.callback_data import CallbackData


class RentCallback(CallbackData, prefix='rent'):
    current_answer: str
    answer_data: str
