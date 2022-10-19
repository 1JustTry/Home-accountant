from datetime import datetime, timedelta
import sys
import textwrap

from .import storage
from .import helpers
#Запрос из БД ID платежа
def input_payment():
    payment_id = helpers.input_int('Введите ID платежа')
    payment = storage.get_payment(payment_id)
    if payment is None:
        print(f'Задача с ID {payment_id} не найдена')
    return payment
# Вводимая информация от пользователя
def input_payment_data(payment=None):
    if payment is not None:
        payment = dict(payment)
    else:
        payment = {}
    data = {}
    data['payment_description'] = helpers.promt('Наименование платежа', default=payment.get('payment_description', ''))
    data['price'] = helpers.promt('Цена', default=payment.get('price', 'Сторговались за бесплатно :)'))
    data['quantity'] = helpers.promt('Количество', default=payment.get('quantity', '1'))
    data['planned'] = helpers.input_date('Дата', datetime.today())
    return data


'Функции основного меню'

# Добавить платеж 
def action_create_payment():
    data = input_payment_data()
    storage.create_payment(**data)
    print(f'''Платеж "{data['payment_description']}"создан!''')
#Редактировать платеж
def action_edit_payment():
    payment = input_payment()
    if payment:
        data = input_payment_data(payment)
        storage.update_payment(payment['id'], **data)
        print(f'''Задача"{data['payment_description']}" успешно отредактирована''')
#Показать все платежи
def action_show_all_payments():
    all_payments = storage.show_payment()
    helpers.print_table(
        ['ID','Наименование платежа','Цена','Количество','Стоимость'], all_payments
    )
#Показать топ платежей с запросом на сортировку по количеству
def action_show_top_payments():
    how_much = helpers.input_int('Сколько платежей выводить?')
    payments = storage.get_top_payments(how_much)
    helpers.print_table(
        ['ID','Наименование платежа','Цена','Количество','Стоимость'], payments
    )
#Показать все платежи за период:
def action_show_all_payments_per_date():
    planned_under = helpers.input_date('Введите дату начала периода')
    planned_after = helpers.input_date('Введите дату конца периода')
    payments = storage.get_payment_per_two_date(planned_under,planned_after)
    helpers.print_table(
        ['ID','Наименование платежа','Цена','Количество','Стоимость'], payments
    )


'Дополнительно выводимые функции для усвоения'
# Вывести платеж за указанную дату
def action_show_payment_per_date():
    planned = helpers.input_date('Введите дату', default=datetime.today())
    payments = storage.get_payment_per_date(planned)
    helpers.print_table(
        ['ID','Наименование платежа','Цена','Количество','Дата'], payments
    )
#Вывести платеж по ID
def action_show_payment_per_id():
    payment_id = str(helpers.input_int('Введите ID'))
    payments = storage.get_payment_per_id(payment_id)
    helpers.print_table(
        ['ID','Наименование платежа','Цена','Количество','Дата'], payments
    )


'Функции интерфейса'
#Показать меню:
def action_show_menu():

    print(textwrap.dedent('''
    1. Добавить платеж
    2. Отредактировать платеж
    3. Вывести все платежи
    4. Вывести все платежи за указанный период
    5. Вывести топ самых крупных платежей
    6. Вывести платеж по Дате
    7. Вывести платеж по ID
    m. Показать меню
    q. Выйти'''))

# Действие:выход
def action_exit():
    sys.exit(0)

actions = {
    '1': action_create_payment,
    '2': action_edit_payment,
    '3': action_show_all_payments,
    '4': action_show_all_payments_per_date,
    '5': action_show_top_payments,
    '6': action_show_payment_per_date,
    '7': action_show_payment_per_id,
    'm': action_show_menu,
    'q': action_exit,
}


#Главная функция
def main():
    storage.initialize(r'task_bookkeeping/resources/schema1.sql')
    action_show_menu()

    while 1:
        cmd = input('\nВведите команду: ')
        action = actions.get(cmd)

        if action is not None:
            action()
        else:
            print('Неизвестная команда')