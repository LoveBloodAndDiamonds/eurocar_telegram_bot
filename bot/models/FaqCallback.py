from aiogram.filters.callback_data import CallbackData


class FaqCallback(CallbackData, prefix='faq'):
    answer: str
