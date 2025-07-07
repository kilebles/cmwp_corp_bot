from aiogram.fsm.state import StatesGroup, State


class Consult(StatesGroup):
    waiting_context = State()
