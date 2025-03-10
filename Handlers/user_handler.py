from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from DataBase.crud import get_register_table_true, get_register_table_false

router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    await state.clear()
    
    welcome_message = (
        "🌸 Добро пожаловать в бота для бронирования столиков в «Япона Хата»! 🌸\n\n"
        "Здесь вы можете легко забронировать столик и управлять своими бронированиями.\n\n"
        "Доступные команды:\n"
        "📅 /book — Начать бронирование столика\n"
        "📋 /my_bookings — Посмотреть ваши бронирования\n"
        "❌ /cancel_booking <ID> — Отменить бронирование\n"
        "💳 /pay <ID> — Оплатить бронь\n\n"
        "Выберите действие и наслаждайтесь удобством! 🍣"
    )
    await message.answer(text=welcome_message)

@router.message(Command('my_bookings'))
async def bookings_get_cmd(message: Message,state: FSMContext):
    await state.clear()

    tg_id = message.chat.id
    result_true = await get_register_table_true(tg_id)
    result_false = await get_register_table_false(tg_id)

    txt = '\n\nОплаченные брони\n\n'
    for key, value in result_true.items():
        if len(value) != 0 and key is not None:
            txt += (f'\nID Брони: {key}'
                    f'\nTG_ID: {value.get('user_id')}'
                    f'\nИмя: {value.get('name')}'
                    f'\nТелефон: {value.get('phone')}'
                    f'\nВремя бронирования: {value.get('date_time')}'
                    f'\nКоличество Людей: {value.get('people_count')}'
                    f'\nСтатус: {value.get('paid')}')
    await message.answer(text=f'{txt}')

    txt = '\n\nНе оплаченные брони\n\n'
    for key, value in result_false.items():
        if len(value) != 0 and key is not None:
            txt += (f'\nID Брони: {key}'
                    f'\nTG_ID: {value.get('user_id')}'
                    f'\nИмя: {value.get('name')}'
                    f'\nТелефон: {value.get('phone')}'
                    f'\nВремя бронирования: {value.get('date_time')}'
                    f'\nКоличество Людей: {value.get('people_count')}'
                    f'\nСтатус: {value.get('paid')}')
    await message.answer(text=f'{txt}')
