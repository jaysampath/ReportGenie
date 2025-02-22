import streamlit as st
import vertica_python
import pandas as pd
from sqlalchemy import create_engine

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
def fetch_schemas():
  try:
    with vertica_python.connect(**conn_info) as connection:
         cursor = connection.cursor() 
         cursor.execute("SELECT schema_name FROM v_catalog.schemata") 
         schemas = cursor.fetchall()
         return [schema [0] for schema in schemas]
  except Exception as e:
    st.error(f"Error fetching schema details: {e}")
    return []
def fetch_tables (schema_name):
  try:
    with vertica_python.connect(**conn_info) as connection:
      cursor = connection.cursor()
      cursor.execute(f"SELECT table_name FROM v_catalog.tables WHERE table_schema = {schema_name}")
      tables = cursor.fetchall()
      return [table [0] for table in tables]
  except Exception as e:
    st.error(f"Error fetching table details: {e}")
    return []
