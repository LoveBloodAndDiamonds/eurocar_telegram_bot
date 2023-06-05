from aiogram.filters.state import StatesGroup, State


class RentAutoState(StatesGroup):
    """
    Класс состояний пользователя при подборе авто.
    """
    USER_REAL_NAME = State()
    REGION = State()
    START_DATE = State()
    END_DATE = State()
    RENT_DAYS = State()
    CAR_CLASS = State()
    CAR_MODEL = State()
    CONFIRM_ORDER = State()
    PHONE_NUMBER = State()
    # CAR_PARK = State()  # Вернуть, когда будет необходимость подключать аффилированные бренды
