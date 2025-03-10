from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


request_button = KeyboardButton(text="Поделиться номером 📞", request_contact=True)

reply_contact_button = ReplyKeyboardMarkup(keyboard=[[request_button]], resize_keyboard=True, one_time_keyboard=True)