from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from DataBase.crud import checking_reg_table, close_order_table
from States.user_state import BuyOrderStater

router = Router()

@router.message(F.text.startswith('/cancel_booking'))
async def cancel_booking_cmd(message: Message, state: FSMContext):
    await state.clear()
    cancel_instruction = ("❌ **Отмена бронирования столика** ❌\n\n"
    "Чтобы отменить бронирование, введите команду следующим образом:\n\n"
    "`/cancel_booking <ID>`\n\n"
    "Где `<ID>` — это **айди вашего заказа**.\n\n"
    "Пример: `/cancel_booking 12345`\n\n"
    "⚠️ **Внимание!** Средства, потраченные на бронирование, **не возвращаются**.\n\n"
    "📋 /my_bookings — Посмотреть ваши бронирования\n\n"
    "Если у вас возникли вопросы, напишите нам! 😊")

    await state.set_state(BuyOrderStater.order_id)
    try:
        id_in_text = int(message.text.replace('/cancel_booking', ''))
    except ValueError:
        await message.answer(text=cancel_instruction)
    else:
        check_id = await checking_reg_table(message.chat.id, id_in_text)

        if check_id:
            await state.update_data(order_id=id_in_text)
            data = await state.get_data()
            order_id = data.get('order_id')
            user_id = message.chat.id
            await close_order_table(user_id=user_id, order_id=order_id)
            await message.answer("✅ **Столик с ID успешно удален!** ✅\n\n"
                                "Спасибо, что воспользовались нашим сервисом!\n\n"
                                "Мы будем рады видеть вас снова в **Япона Хата**! 🍣\n\n"
                                "До встречи! 😊")
        else:
            await message.answer(text=cancel_instruction)
    finally:
        await state.clear()
