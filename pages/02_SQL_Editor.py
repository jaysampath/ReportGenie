import streamlit as st
from streamlit_ace import st ace, KEYBINDINGS, LANGUAGES, THEMES
import streamlit_toggle as tog
import vertica_python
import pandas as pd
import utils
st.set_page_config(page_title="ReportGenie", page_icon="")
st.header('SQL Editor')
supported_tables = ['MerchantTransactions']
# result_tables = f"({', '.join(f'\'{entry}\'' for entry in supported_tables)})"
result_tables = "('" + "', '".join(supported_tables) + "')"
target_schema = 'MERCH'
print("result-tables")
print(result_tables)
#Vertica connection configuration
conn_info = {
'host': 'vertica.db.host',
'port': '5433',
'user': 'username',
'password': 'xxxx',
'dbname': 'vertica' # Replace with your actual database name
}
def create_connection():
  return vertica_python.connect(**conn_info)
def get_tables_and_columns():
  conn = create_connection()
  cursor =conn.cursor()
  #Fetch the list of all tables
  cursor.execute(f"SELECT table_name FROM v_catalog.tables WHERE table_schema = {target_schema} and table_name in (result_tables)")
  tables = cursor.fetchall()
  print("tables")
  #print(tables)
  table_column_mapping = {}
  for table in tables:
    table_name = table[0]
    #Fetch column names for each table
    cursor.execute(f"SELECT column_name, data_type FROM v_catalog.columns WHERE table_schema '{target_schema}' AND table_name = '{table_name}'")
    #columns_info cursor.fetchall()
    #cursor.execute(f"PRAGMA table_info({table_name});")
    columns = [(col [8],col[1]) for col in cursor.fetchall()]
    table_column_mapping[table_name] = columns
  conn.close()
  return table_column_mapping
def query():
  display_tables()
  #st.subheader("Query Editor")
  #initialize session dict
  if "sql_editor_queries" not in st.session_state:
    st.session_state ["sql_editor_queries"] = [{"role": "assistant", "content": "How can I help you?"}]
    content = st_ace(
    value=st.session_state['current_query'],
    placeholder="--Select Database and Write your SQL Query Here!",
    language= 'sql',
    #theme='light',
    keybinding=KEYBINDINGS[3],
    font_size=15,
    min_lines=15,
    key="run_query",
    height=200 )
  if content:
    #st.subheader("Content")
    #st.text(content)
    # def next_page():
    # st.switch_page("pages/gen_ai_reporting.py")
    def run_query():
      query = content
      conn = create_connection()
  try:
    cursor = conn.cursor()
    cursor.execute(f"SET SEARCH_PATH TO {target_schema}") # To query only MERCH schema
    query= cursor.execute(query)
    cols = [column[0] for column in query.description]
    results_df= pd.DataFrame.from_records (
    data = query.fetchall(),
    columns = cols
    )
    st.dataframe (results_df)
    export = results_df.to_csv()
    st.download_button(label="Download Results", data=export, file_name='query_results.csv')
    st.button('Save The Query', on_click=save_query, args=[content])
    st.button('Schedule A Report', on_click=schedule_report, args=[content], type="primary")
  except Exception as e:
    st.write(e)
  st.write("Results")
  run_query()
  #next_page()
def save_query(query):
  if "query_history" in st.session_state:
    st.session_state.query_history.append(query)
def schedule_report(query):
  report_trigger_response =utils.generate_report(query)
  report_trigger_display_text = "Scheduled a report through reporting service. Here is the subscription metadata"
  st.session_state.sql_editor_queries.append({"role": "assistant", " content": report_trigger_display_text})
  st.session_state.sql_editor_queries.append({"role": "assistant", "json": report_trigger_response))
  st.session_state.configured_schedules.append(report_trigger_response)
  st.session_state ["current_query"] = query
  st.write(report_trigger_display_text)
  st.json(report_trigger_response)
def display_tables():
  tables_and_columns = get_tables_and_columns()
  #Simulating treeview with expanders for tables and checkboxes for columns
  #st.header("Available Tables")
  with st.sidebar:
    st.header("Available Tables and Columกร")
    for table_name, columns in tables_and_columns.items():
      with st.expander(table_name, expanded=False): # Expander acts like a collapsible panel
        for col_name,col_type in columns:
          st.write(f"{col_name} ({col_type})") # List columns under each table
def get_suggestions (query, tables_and_columns):
  suggestions = set()
  for table_name, columns in tables_and_columns.items():
    if table_name.lower().startswith(query.lower()):
      suggestions.add(table_name)
  for column in columns:
    if column.lower().startswith(query.lower()):
      suggestions.add(column)
  return sorted(suggestions)
if __name__ == "__main__":
  if "logged_in" not in st.session_state:
    st.write('Please login in Home Page to continue.')
  elif st.session_state.logged_in == False:
    st.write('You need to login to continue using it. Please go to Home Page to login')
  else:
    query()
