from aiogram.dispatcher.filters.state import State, StatesGroup
class State_book_a_room(StatesGroup):
    check_in_date = State()
    check_out_date = State()
    room_number = State()

class state_food_order(StatesGroup):
    name = State()
    room = State()

class state_housekeeping(StatesGroup):
    name = State()
    room = State()

class state_ask_adminstration(StatesGroup):
    ask = State()

class state_answer_admin(StatesGroup):
    msg_id = State()
    user_id = State()
    answer = State()
