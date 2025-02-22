import utils
import os
import re
import sqlite3
import streamlit as st
from streamlit.logger import get_logger
from pathlib import Path
from sqlalchemy import create_engine
import vertica_python
import pandas as pd
import json
import history
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from Query Approve import Query Approve
from query.query_service import QueryService
from templates.prompt_template import get_schema
from vertica_utils import fetch_schemas, fetch_tables, fetch_columns
from langchain_core.prompts import PromptTemplate
from templates.prompt_template import get_template
from json_utils import clean_json_output
logger = get_logger('Langchain-Chatbot')
st.set_page_config(page_title="ReportGenie", page_icon="")
st.header('Chat with AI for your reporting requirements')
st.write('Enable the chatbot to interpret your query and generate a report')
st.sidebar.header('Database Schema Details')
os.environ ["DATABRICKS_HOST"]='https://dbc-d587060f-4371.cloud.databricks.com'
os.environ ["DATABRICKS_TOKEN"]=''
DATABRICKS_TOKEN = ''
selected_query = None
supported_tables = ['Transactions', 'MerchantDemographics', 'Chargebacks', 'MerchantFunding']
# result_tables = f"({', '.join(f'\'{entry}\' for entry in supported_tables)})"
result_tables = "('" + "', '".join(supported_tables) + "')"
target_schema = 'BI'
print("result tables")
print(result_tables)
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
def create_connection():
    return vertica_python.connect(**conn_info)
def get_tables_and_columns():
  conn = create_connection()
  cursor = conn.cursor()
  # Fetch the list of all tables
  cursor.execute (f"SELECT table_name FROM v_catalog.tables WHERE table_schema '{target_schema}' and table_name in {result_tables}")
  tables = cursor.fetchall()
  print("tables")
  #print(tables)
  table_column_mapping = {}
  for table in tables:
    table_name = table[0]
    #Fetch column names for each table
    cursor.execute(f"SELECT column_name, data_type FROM v_catalog.columns WHERE table_schema = '{target_schema}' AND 'table_name = '{table_name}'")
    # columns_info = cursor.fetchall()
    #cursor.execute (f"PRAGMA table_info({table_name});")
    columns = [(col[0], col[1]) for col in cursor.fetchall()]
    table_column_mapping [table_name] = columns
  conn.close()
  return table_column_mapping
def display_tables():
  tables_and_columns = get_tables_and_columns()
  #Simulating treeview with expanders for tables and checkboxes for columns
  #st.header("Available Tables")
  with st.sidebar:
    st.header("Available Tables and Columns")
    for table_name, columns in tables_and_columns.items():
      with st.expander (table_name, expanded=False): # Expander acts like a collapsible panel
        for col_name,col_type in columns:
          st.write(f"{col_name} ({col_type})") # List columns under each table
class SqlChatbot:
  def __init__(self):
    utils.sync_st_session()
    self.llm = utils.configure_llm()
  @st.cache_resource
  def setup_chain(_self):
    memory = ConversationBufferMemory()
    chain = ConversationChain(llm=_self.llm, memory=memory, verbose=False)
    return chain
  def extract_query_from_llm_text_response(_self, llm_response):
    json_pattern= r'((.*})'
    #Search for JSON in the input string
    match = re.search(json_pattern, llm_response, re.DOTALL)
    if match:
      json_body = match.group (1)
    try:
      #Parse the JSON body 
      data= json.loads(json_body)
      #Extract and return the query return data.get('query', None)
    except json.JSONDecodeError:
      print('error')
    pattern = r'(?<=query":\s") [\s\S]+(?="\n)'
    # Extract the query
    query= re.search(pattern, llm_response)
    if query:
      return query.group().strip()
    #from utils
    from_utils = utils.extract_sql_query(llm_response)
    if from_utils:
      return from_utils
    return None
  @utils.enable_chat_history
  def main(self):
    chain = self.setup_chain()
    query_service = QueryService(model=self.llm)
    query_service = QueryService(model=self.llm)
    user_query= st.chat_input(placeholder="Ask me anything!")
    if user_query:
      st.session_state.messages.append({"role": "user", "content": user_query})
      st.chat_message("user").write(user_query)
      with st.chat_message("assistant"):
        self.remove_stale_buttons()
        st_cb = StreamlitCallbackHandler(st.container())
        tables=['Transactions', 'MerchantFunding']
        schema_for_template = get_schema (tables)
        prompt = PromptTemplate.from_template(get_template())
        template = get_template()
        final_llm_input = template.format(question=user_query, schema=schema_for_template, MerchantNumber= utils.get_merchant_number())
        #chain2 = prompt | self.llm
        #result = chain2.invoke({"question": user query, "schema": schema_for_template, "MerchantNumber": utils.get_merchant_number(
        result = chain.invoke(("input":final_llm_input},
                 {"callbacks": [st_cb]})
        logger.info(f"LLM Result: {result['response']}")
        response = result["response"]
        query_from_json = self.extract_query_from_llm_text_response (response)
        print('--query_from_json', query_from_json)
        display_sql = "Here is the SQL query for your report.\n"
        #st.code(body-query_from_json, language="sql", line_numbers=True)
        sql = """``` sql {query_from_json} ```"""
        markdown_sql = sql.format(query_from_json=query_from_json)
        print('markdown', markdown_sql)
        def format_sql(query):
          keywords = ['SELECT', 'FROM', 'WHERE', 'ORDER BY', 'GROUP BY', 'HAVING', 'JOIN', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'ON'] 
          pattern = re.compile(r'\b'+'|'.join(keywords) + r')\b', re. IGNORECASE)
          formatted_query = pattern.sub(r'\n\1', query)
          return formatted_query.strip()
        formatted_sql = format_sql(query_from_json)
        st.code(body=formatted_sql, language="sql", line_numbers=True)
        #st.markdown (markdown_sql)
        if query_from_json:
          st.session_state.messages.append({"role": "assistant", "content": display_sql+""+str(query_from_json) + ""})
          approve_button = st.button("Run Query", on_click=self.approved_sql_query_post_process, args=[query_from_json, query_service], type="primary")
          save_query_button = st.button("Save Query", on_click=self.save_query, args=[query_from_json])
        else:
          no_query_text="*could not generate an sql query from your query. Please try re-framing the prompt*"
          st.write(no_query_text)
          st.session_state.messages.append({"role": "assistant", "content": no_query_text})
  def approved_sql_query_post_process(self, query, query_service):
    print('Approve button clicked, user Approved SQL Query.')
    print('Executing SQL query, query')
    preview_content='Here are the query results.'
    st.session_state.messages.append({"role": "assistant", "content": preview_content})
    results_preview, col_names = query_service.execute_query(query.replace('',''))
    if results_preview:
      if results_preview:
        st.session_state.messages.append({"role":"assistant", "dataframe": results_preview, "col_names" :col_names})
        st.session_state.messages.append({"unique_term":"unique_term", "role": "assistant", "button": "Data looks good!. Schedule & Report", "on_click" : self.generate_report, "args" : [query], "disabled": False})
      else:
        no_query_text="The query does not return any records. Please try again with another prompt"
        st.write(no_query_text)
        st.session_state.messages.append({"role": "assistant", "content": no_query_text})
  
  def generate_report(self, query):
    print('Creating report config.....')
    report_trigger_response = utils.generate_report(query.replace())
    if report_trigger_response:
      report_trigger_display_text = "Scheduled a report through Reporting servicel. Your report will be triggered DAILY at 10AM UTC. report_trigger_display_text += "Please check your SFTP path" str(utils.get_merchant_number()) "/reports for the report.
      report_trigger_display_text += "Please note that the approximate report delivery time is 5-10min. Here is the subscription metadata"
      st.session_state.messages.append({"role": "assistant", "content": report_trigger_display_text})
      st.session_state.messages.append({"role": "assistant", "json": report_trigger_response})
      st.session_state.configured_schedules.append(report_trigger_response)
    else:
      no_report_display_text="*Couldn't generate a report with your query. Please retry or re-frame your query"
      st.session_state.messages.append({"role": "assistant", "content": no_report_display_text})
      self.remove_generate_button_from_messages()
  
  if selected_query and selected_query != "Select Query":
    st.sidebar.subheader("Selected Query Response")
    st.sidebar.write(f"Query: {selected_query}")
  
  def remove_generate_button_from_messages(_self):
    for msg in st.session_state["messages"]:
      if "unique_term" in msg:
        if "button" in msg:
          del msg["button"]
          msg["content"] = "*Scheduled the report!*"
  
  def remove_stale_buttons(self):
    for msg in st.session_state["messages"]:
      if "unique_term" in msg: 
        if "disabled" in msg: 
          if msg["disabled"] == False:
            st.session_state ["messages"].remove(msg)
  
  def save_query(self, query):
    if "query_history" in st.session_state:
      st.session_state.query_history.append(query)

if __name__ == "__main__":
  if "logged_in" not in st.session_state:
    st.write('Please login in Home Page to continue.')
  elif st.session_state.logged_in == False:
    st.write('You need to login to continue using it. Please go to Home Page to login')
  else:
    display_tables()
    obj = SqlChatbot()
    obj.main()
