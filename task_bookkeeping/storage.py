from datetime import datetime, time
from .services import make_db_connection 
'Блок переменных по запросам из базы SQLite3'
#Создать новый платеж
SQL_CREATE_NEW_PAYMENT = 'INSERT INTO payment(payment_description,  price, quantity, planned) VALUES (?,?,?,?)'
#Отредактировать платеж
SQL_EDIT_PAYMENT = 'UPDATE payment SET payment_description=?, price=?, quantity=?, planned=? WHERE id=?'
#Выбрать все платежи
SQL_SELECT_ALL_PAYMENTS = 'SELECT id, payment_description,  price, quantity, planned FROM payment'
#Вывести все платежи за укказанную дату
SQL_SHOW_ALL_PAYMENTS_PER_DATE = f'{SQL_SELECT_ALL_PAYMENTS} WHERE planned BETWEEN ? AND ?'
#Вывести топ платежей по стоимости
SQL_SHOW_TOP_PAYMENTS = 'SELECT id, payment_description, price,quantity, price * quantity AS cost FROM payment ORDER BY cost DESC LIMIT ?'
#Вывести платеж по его ID}
SQL_SHOW_PAYMENT_BY_ID = f'{SQL_SELECT_ALL_PAYMENTS} WHERE id=?' 
#Вывести всю БД
SQL_SHOW_PAYMENT = 'SELECT id, payment_description, price,quantity, price * quantity AS cost FROM payment'
#Вывести все платежи в промежуток
SQL_SHOW_ALL_PAYMENTS_PER_TWO_DATE = 'SELECT id, payment_description, price,quantity, price * quantity AS cost FROM payment WHERE planned BETWEEN ? AND ?'


def initialize(creation_schema):
    with make_db_connection() as conn:
        with open(creation_schema) as f:
            conn.executescript(f.read())

#Запрос по ID 
def get_payment(payment_id):
    with make_db_connection() as conn:
        return conn.execute(SQL_SHOW_PAYMENT_BY_ID, (payment_id,)).fetchone()
#Вывести плтеж по ID
def get_all_arg_payment(payment_id, payment_description,  price, planned, quantity):
    with make_db_connection() as conn:
        return conn.execute(SQL_SHOW_PAYMENT_BY_ID, (payment_id,payment_description,  price, planned, quantity)).fetchone()
#Создать новый платеж
def create_payment(payment_description,  price, planned, quantity=1):
    with make_db_connection() as conn:
        conn.execute(SQL_CREATE_NEW_PAYMENT, (payment_description,  price, quantity, planned))

#Платеж за указанную дату
def get_payment_per_date(dt):
    dt = datetime.combine(dt,time())
    dt_end = datetime.combine(dt, time(23,59,59))
    with make_db_connection() as conn:
        cursor = conn.execute(SQL_SHOW_ALL_PAYMENTS_PER_DATE, (dt, dt_end))
        return cursor.fetchall()
#Редактирование платежа
def update_payment(payment_id, payment_description,  price, quantity, planned):
    with make_db_connection() as conn:
        conn.execute(SQL_EDIT_PAYMENT, (payment_description,  price, quantity, planned, payment_id))


#Запрос на ТОП с сортировкой
def get_top_payments(how_much):
    with make_db_connection() as conn:
        cursor = conn.execute(SQL_SHOW_TOP_PAYMENTS, (how_much,))
        return cursor.fetchall()

# Запрос всего из БД
def show_payment():
    with make_db_connection() as conn:
        cursor = conn.execute(SQL_SHOW_PAYMENT)
        return cursor.fetchall()

#Для запроса по ID тест
def get_payment_per_id(payment_id):
    with make_db_connection() as conn:
        cursor = conn.execute(SQL_SHOW_PAYMENT_BY_ID, (payment_id,))
        return cursor.fetchall()

# Платеж за определенный период времени
def get_payment_per_two_date(dt, dt_end):
    # dt = datetime.date()
    # dt_end = datetime.date()
    with make_db_connection() as conn:
        cursor = conn.execute(SQL_SHOW_ALL_PAYMENTS_PER_TWO_DATE, (dt, dt_end))
        return cursor.fetchall()