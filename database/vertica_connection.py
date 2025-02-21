import sqlalchemy as sa
from langchain_community.utilities.sql_database import SQLDatabase
import vertica_python

VERTICA_USERNAME = ''
VERTICA_PASSWORD = ''

def get_db_connection():
    conn_info = {
        'host' : 'vertica.db.host',
        'port': 5433,
        'user' : VERTICA_USERNAME,
        'password' : VERTICA_PASSWORD,
        'read_timeout' : 600,
        'database' : 'testdb',
        'ssl' : False,
        'connection_timeout' : 30

    }

    connection = vertica_python.connect(**conn_info)
    return connection