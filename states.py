from aiogram.fsm.state import State, StatesGroup

class CalcFlowState(StatesGroup):
    waiting_for_custom_model = State()
    waiting_for_booking_phone = State()
