from aiogram.filters.state import State


class RentAutoState(State):
    REGION = State()
    CAR_CLASS = State()
    CAR_PARK = State()
    CAR = State()
