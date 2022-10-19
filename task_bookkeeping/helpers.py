import textwrap
from datetime import datetime
import os

from prettytable import PrettyTable

__all__ =(
    'input_datetime', 'input_date','input_int','input_float', 'print_table'
)

def promt(msg, default=None, type_cast=None):
    while 1:
        value = input(f'{msg}: ')
        if not value:
            return default
        
        if type_cast is None:
            return value
        
        try:
            return type_cast(value)
        except ValueError as err:
            print(err)

def input_int(msg='Введите число', default=None,):
    return promt(msg, default, type_cast=int)

def input_float(msg='Введите число', default=None,):
    return promt(msg, default, type_cast=float)


'''Тут я немного решил по-тупому схитрить и поставил формат у date value как %Y-%m-%d %H:%M:%S с обязательным вводом времени. 
Ошибка с ValueError: not enough values to unpack (expected 2, got 1) угнетала меня очень долгое время.'''

def input_date(msg='Введите дату', default=None, fmt= '%Y-%m-%d %H:%M:%S'):
    return promt(msg, default, type_cast = lambda value: datetime.strptime(value, fmt))

# def input_date(msg='Введите дату', default=None, fmt= '%Y-%m-%d %H:%M:%S'):
#     return promt(msg, default, type_cast = lambda value: datetime.strptime(value, fmt).date())

#Печать таблицы 
def print_table(headers, iterable):
    table = PrettyTable(headers)
    for row in iterable:
        table.add_row(row)
    print(table)
    
