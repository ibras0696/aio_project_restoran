import asyncio
import sqlite3

BASE_NAME = './DataBase/BaseRest.db'
OrderSale = 'OrderSale'


# Функция для бронирования
async def register_table_rest(
        user_id: int,
        name: str,
        phone: str,
        date_time: str,
        people_count: int,
        paid: bool = False):
    with sqlite3.connect(BASE_NAME) as con:
        cur = con.cursor()
        cur.execute(f'''
        INSERT INTO {OrderSale}(user_id, name, phone, date_time, people_count, paid)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, name, phone, date_time, people_count, paid))
        con.commit()

        return True


# Функция для получения бронированных столиков
async def get_register_table_true(user_id: int):
    '''

    :param user_id:
    :return:  {2: {'user_id': 2, 'name': 'Ибра', 'phone': '79323056361', 'date_time': '01 04 2025', 'people_count': 10, 'paid': 1}}
    '''
    with sqlite3.connect(BASE_NAME) as con:
        cur = con.cursor()
        items = cur.execute(f"SELECT * FROM {OrderSale} WHERE user_id == ? AND paid == True", (user_id, )).fetchall()
        if len(items) == 0:
            return {}
        result = {
            i[0]: {
                'user_id': i[1],
                'name': i[2],
                'phone': i[3],
                'date_time': i[4],
                'people_count': i[5],
                'paid': i[6]
            }
            for i in items
        }
        return result

# Функция для получения Не оплаченных столиков
async def get_register_table_false(user_id: int):
    '''

    :param user_id:
    :return:  {2: {'user_id': 2, 'name': 'Ибра', 'phone': '79323056361', 'date_time': '01 04 2025', 'people_count': 10, 'paid': 1}}
    '''
    with sqlite3.connect(BASE_NAME) as con:
        cur = con.cursor()
        items = cur.execute(f"SELECT * FROM {OrderSale} WHERE user_id == ? AND paid == False", (user_id, )).fetchall()
        if len(items) == 0:
            return {}
        result = {
            i[0]: {
                'user_id': i[1],
                'name': i[2],
                'phone': i[3],
                'date_time': i[4],
                'people_count': i[5],
                'paid': i[6]
            }
            for i in items
        }
        return result


# Проверка есть ли Ордер в БД
async def checking_reg_table(user_id: int, order_id: int):
    '''

    :param user_id: Айди пользователя
    :param order_id: Айди платежа
    :return:
    '''
    with sqlite3.connect(BASE_NAME) as con:
        cur = con.cursor()
        items = cur.execute(f"SELECT id FROM {OrderSale} WHERE user_id == ? AND id == ?", (user_id, order_id)).fetchall()
        if len(items) == 0:
            return False
        else:
            return True


async def close_order_table(user_id: int, order_id: int):
    with sqlite3.connect(BASE_NAME) as con:
        cur = con.cursor()

        cur.execute(f"DELETE FROM {OrderSale} WHERE id == ? AND user_id == ?", (order_id, user_id))

        con.commit()

        return True


# Функция для обновления статуса на True
async def update_status_table(user_id: int, order_id: int):
    with sqlite3.connect(BASE_NAME) as con:
        cur = con.cursor()
        cur.execute(f'''
        UPDATE {OrderSale}
        SET paid == True
        WHERE id == ? AND user_id == ?
        ''', (order_id, user_id))

        con.commit()
        return True



