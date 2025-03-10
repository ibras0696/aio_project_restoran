from datetime import datetime

async def check_datetime_format(input_string):
    try:
        # Пытаемся преобразовать строку в объект datetime
        datetime.strptime(input_string, '%H:%M-%d.%m.%y')
        return True
    except ValueError:
        # Если возникает ошибка, значит формат неверный
        return False


