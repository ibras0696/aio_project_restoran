import dotenv
import os


# Загрузка данных с .env
dotenv.load_dotenv()

# Получение Токена
bot_token = os.getenv('TOKEN')

# Получение токена для оплаты
PAYMENTS_TOKEN = os.getenv('PAYMENTS_TOKEN')