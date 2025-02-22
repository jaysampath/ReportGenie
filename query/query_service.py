import datetime
import decimal
from langchain.chains import create_sql_query_chain
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from models.response import Response
from database.vertica_connection import get_db_connection
from models.response import Response
from templates.prompt_template import get_template
from templates.prompt_template import get_schema
from helpers.logger import get_logger
from vertica_utils import fetch_schemas, fetch_tables, fetch_columns
from json_utils import clean_json_output
import streamlit as st
logger = get_logger(__name__)
class QueryService:
  def __init__(self, model):
    self.db = get_db_connection()
    self.llm = model
def generate_query(self, st_cb, question) -> Response:
  #tables = fetch_tables(schema)
  schema = 'BI'
  tables=['Transactions', 'MerchantFunding']
  schema_for_template = get_schema (tables)
  print('---schema_for_template', schema_for_template)
  prompt = PromptTemplate.from_template(get_template())
  chain = prompt | self.llm
  result = chain.invoke({"question": question, "schema": schema_for_template}, {"callbacks": [st_cb]})
  logger.info(f"LLM Result: {result.content}")
  cleaned_result = clean_json_output(result.content)
  return result.content
def build_schema (self, schema_name, tables):
  schema="""
  for table_name in tables:
  columns = fetch_columns(schema_name, table_name)
  schema +=
  Table: {table_name}
  columns:
  - {columns}
  """
  return schema
def execute_query(self, query: str):
  try:
    safe_dict={
    'datetime': datetime,
    'Decimal': decimal. Decimal
    }
    cursor = self.db.cursor()
    executable_query = ""
    if ("where" in query) or ("WHERE" in query):
      merchant_number = self.get_merchant_number()
      if merchant_number not in query:
        executable_query= query + " and merchantnumber=" + self.get_merchant_number() + **
    else:
      executable_query = query + "where merchantnumber='" + self.get_merchant_number() + "
    if executable_query:
      limit_query=executable_query
    else:
      limit_query = query
    print("limit query", limit_query)
    result = cursor.execute(limit_query)
    col_names = [column[0] for column in result.description]
    records = cursor.fetchall()
    print('result-', records)
    if len(records) == 0:
      return None, None
    return None, None
  except:
    return None, None
  
def get_merchant_number(Self):
  if "merchantnumber" in st.session_state:
    return st.session_state.merchantnumber
  else:
    return st.session_state.default_merchant_number
