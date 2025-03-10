from aiogram import Router, F
from aiogram import Bot,  types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import LabeledPrice, Message, PreCheckoutQuery

from DataBase.crud import checking_reg_table, update_status_table
from States.user_state import BuyOrderStater

from Handlers.Payments.payments_text import prices, provider_token


router = Router()


# Команда /buy
@router.message(F.text.startswith("/pay"))
async def buy_order_cmd(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(BuyOrderStater.order_id)
    try:
        id_in_text = int(message.text.replace('/pay', ''))
    except ValueError:
        await message.answer("💳 **Введите команду для оплаты:**\n\n"
                             "Пожалуйста, введите команду следующим образом:\n\n"
                             "`/pay <ID>`\n\n"
                             "Где `<ID>` — это **айди вашего заказа**.\n\n"
                             "Пример: `/pay 12345`\n\n"
                             "📋 /my_bookings — Посмотреть ваши бронирования\n\n"
                             "Если у вас возникли вопросы, напишите нам! 😊")
    else:

        check_id = await checking_reg_table(message.chat.id, id_in_text)

        if check_id:
            await state.update_data(order_id=id_in_text)

            # Создаем инвойс (счет)
            title = "Платеж"
            description = "Оплата за Бронирование"
            payload = "Успешный Платеж"  # Уникальный идентификатор платежа
            currency = "RUB"  # Валюта (рубли)

            # Отправляем инвойс
            await message.answer_invoice(
                title=title,
                description=description,
                payload=payload,
                provider_token=provider_token,
                currency=currency,
                prices=prices,
            )
        else:
            await message.answer("💳 **Введите команду для оплаты:**\n\n"
        "Пожалуйста, введите команду следующим образом:\n\n"
        "`/pay <ID>`\n\n"
        "Где `<ID>` — это **айди вашего заказа**.\n\n"
        "Пример: `/pay 12345`\n\n"
        "📋 /my_bookings — Посмотреть ваши бронирования\n\n"
        "Если у вас возникли вопросы, напишите нам! 😊")



# Обработка успешного платежа
@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    # Подтверждаем платеж
    await pre_checkout_query.answer(ok=True)

# Обработка успешной оплаты
@router.message(lambda message: message.successful_payment is not None)
async def process_successful_payment(message: Message, state: FSMContext):
    data = await state.get_data()
    order_id = data.get('order_id')
    await update_status_table(message.chat.id, order_id)
    await message.answer("✅ Платеж успешно завершен! Спасибо за покупку!")
    await state.clear()