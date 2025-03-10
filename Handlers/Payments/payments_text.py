from aiogram.types import LabeledPrice
from config import PAYMENTS_TOKEN

prices = [
        LabeledPrice(label="🍽️Бронирование столика🍽️", amount=15000)  # Сумма в копейках (10000 = 150 рублей)
    ]
provider_token =  PAYMENTS_TOKEN # Тестовый токен Stripe или другой системы