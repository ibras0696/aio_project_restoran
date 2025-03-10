import asyncio
import sqlite3

BASE_NAME = './DataBase/BaseRest.db'
OrderSale = 'OrderSale'

async def create_table():
    with sqlite3.connect(BASE_NAME) as con:
        cur = con.cursor()

        cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {OrderSale}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            phone TEXT,
            date_time TEXT,
            people_count INTEGER,
            paid BOOLEAN
        )
        ''')

        con.commit()