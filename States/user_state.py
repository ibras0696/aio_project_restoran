from aiogram.fsm.state import StatesGroup, State


# Состояние для Регистрации столика
class RegisterOrderState(StatesGroup):
    user_id = State()
    name = State()
    phone = State()
    date_time = State()
    people_count = State()
    paid = State()

# Состояния для Ордера
class BuyOrderStater(StatesGroup):
    order_id = State()