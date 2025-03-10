from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from DataBase.crud import register_table_rest
from Keyboards.user_keyboards import reply_contact_button
# Состояния
from States.user_state import RegisterOrderState

from Handlers.Function.date_function import check_datetime_format

router = Router()


@router.message(Command('book'))
async def book_cmd(message: Message, state: FSMContext):
    # Работа с состояниями
    await state.set_state(RegisterOrderState.name)
    await state.update_data(user_id=message.chat.id)
    await state.update_data(paid=False)

    await message.answer("👤 **Введите ваше имя:**\n\n"
    "Пожалуйста, укажите ваше имя, чтобы мы могли персонализировать ваше бронирование.\n\n"
    "Например: `Ибрахим` или `Санет`.\n\n"
    "Мы рады видеть вас! 😊")


@router.message(RegisterOrderState.name)
async def book_name_cmd(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RegisterOrderState.phone)

    await message.answer(text="📞 **Введите контактный номер для связи:**\n\n"
        "Пожалуйста, укажите ваш номер телефона, чтобы мы могли связаться с вами.\n\n"
        "Например: `+79991234567` или `89991234567`.\n\n"
        "Мы ценим ваше доверие! 😊", reply_markup=reply_contact_button)


@router.message(RegisterOrderState.phone)
async def book_phone_cmd(message: Message, state: FSMContext):
    message_text_send = ("Пожалуйста, введите дату и время в правильном формате:\n\n"
            "🕒 **Пример:** `20:30-01.12.24`\n\n"
            "Этот формат означает:\n"
            "- `20:30` — время (часы:минуты)\n"
            "- `01.12.24` — дата (день.месяц.год)\n\n"
            "Попробуйте еще раз! 😊")
    try:
        await state.update_data(phone=message.contact.phone_number)
    except AttributeError:
        await state.update_data(phone=message.text)
    finally:
        await state.set_state(RegisterOrderState.date_time)
        await message.answer(message_text_send)



@router.message(RegisterOrderState.date_time)
async def book_date_time_cmd(message: Message, state: FSMContext):
    # Проверка правильного ввода даты
    check_data = await check_datetime_format(message.text)
    if check_data:
        await state.update_data(date_time=message.text)
        await state.set_state(RegisterOrderState.people_count)

        await message.answer(text="👥 **Введите количество людей:**\n\n"
        "Пожалуйста, укажите, на сколько человек вы хотите забронировать столик.\n\n"
        "Например: `2` — для двоих, `4` — для компании из четырех человек.\n\n"
        "Мы готовы сделать ваш вечер незабываемым! 🍣")
    else:
        await state.set_state(RegisterOrderState.date_time)
        await message.answer(text="❌ **Неверный формат даты!** ❌\n\n"
        "Пожалуйста, введите дату и время в правильном формате:\n\n"
        "🕒 **Пример:** `20:30-01.12.24`\n\n"
        "Этот формат означает:\n"
        "- `20:30` — время (часы:минуты)\n"
        "- `01.12.24` — дата (день.месяц.год)\n\n"
        "Попробуйте еще раз! 😊")


@router.message(RegisterOrderState.people_count)
async def book_people_count(message: Message, state: FSMContext):
    error_send_message = ("❌ **Ошибка ввода!** ❌\n\n"
    "Пожалуйста, введите данные **в цифрах**.\n\n"
    "Например: `2` — для двоих, `10` — для компании из десяти человек.\n\n"
    "Также Столики Рассчитаны на группу не больше 30 человек! "
    "Попробуйте еще раз! 😊")
    try:
        result_count = int(message.text)
    except ValueError:
        await state.set_state(RegisterOrderState.people_count)
        await message.answer(error_send_message)
    else:
        if result_count < 0 or result_count >= 30:
            await state.set_state(RegisterOrderState.people_count)
            await message.answer(error_send_message)
            return

        await state.update_data(people_count=result_count)

        data_order = await state.get_data()
        user_id = data_order.get('user_id')
        name = data_order.get('name')
        phone = data_order.get('phone')
        date_time = data_order.get('date_time')
        people_count = data_order.get('people_count')

        # Функция для записи Брони в БД
        await register_table_rest(
            user_id=user_id,
            name=name,
            phone=phone,
            date_time=date_time,
            people_count=people_count
        )

        await message.answer(text="🎉 **Бронирование успешно выполнено!** 🎉\n\n"
            "Теперь вы можете перейти к оплате. Для этого введите команду:\n\n"
            "💳 `/pay <ID>` — чтобы оплатить бронирование.\n\n"
            "Спасибо за выбор нашего сервиса! Мы ждем вас! 🍣")

        await state.clear()
