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


    for key, value in result_true.items():
        txt = '\n\nОплаченные брони\n\n'
        if len(value) != 0 and key is not None:
            txt += (f'\n🔷 ID Брони: {key}'
                    f'\n👤 TG_ID: {value.get('user_id')}'
                    f'\n📛 Имя: {value.get('name')}'
                    f'\n📞 Телефон: {value.get('phone')}'
                    f'\n⏰ Время бронирования: {value.get('date_time')}'
                    f'\n👥 Количество людей: {value.get('people_count')}'
                    f'\n💰 Статус: {"✅ Оплачено" if value.get('paid') else "❌ Не оплачено"}')
        await message.answer(text=f'{txt}')


    for key, value in result_false.items():
        txt = '\n\nНе оплаченные брони\n\n'
        if len(value) != 0 and key is not None:
            txt += (f'\n🔷 ID Брони: {key}'
                    f'\n👤 TG_ID: {value.get('user_id')}'
                    f'\n📛 Имя: {value.get('name')}'
                    f'\n📞 Телефон: {value.get('phone')}'
                    f'\n⏰ Время бронирования: {value.get('date_time')}'
                    f'\n👥 Количество людей: {value.get('people_count')}'
                    f'\n💰 Статус: {"✅ Оплачено" if value.get('paid') else "❌ Не оплачено"}')
        await message.answer(text=f'{txt}')
