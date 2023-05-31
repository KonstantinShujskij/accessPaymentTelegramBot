from aiogram.dispatcher.filters.state import StatesGroup, State


class allow_access_state(StatesGroup):
    telegram = State()
    name = State()
    course = State()
    min = State()
    max = State()


class report_state(StatesGroup):
    partner = State()
    start_date = State()
    stop_date = State()
