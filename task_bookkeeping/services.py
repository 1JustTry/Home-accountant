
from configparser import ConfigParser
from datetime import datetime
import sqlite3


def make_config(*config_files):
    config = ConfigParser()
    config.read(config_files)
    return config


default_config = make_config(r'task_bookkeeping/resources/config.ini')

def make_db_connection():
    db_name = default_config.get('db', 'db_name')

    with sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
        conn.row_factory = sqlite3.Row

        sqlite3.register_converter(
            'DATE',
            lambda value: datetime.strptime(value.decode(), '%Y-%m-%d')
        )
        sqlite3.register_converter(
            'DATETIME',
            lambda value: datetime.strptime(value.decode(), '%Y-%m-%d %H:%M:%S')
        )

        return conn
