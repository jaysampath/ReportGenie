import streamlit as st
st.session_state['current_query'] = "Select * from BI. Transactions t where t.StatementDate=2020-86-84'"
st.session_state['configured schedules'] = []
st.session_state['query_history']=[]
st.session_state['default_merchant_number'] = '3286000000292144'
st.session_state['current_page']='Home'
st.set_page_config(page_title="ReportGenie", page_icon="B")
st.header('ReportGenie')
#Initialize session state for merchantnumber and login status
if 'logged_in' not in st.session_state:
  st.session_state.logged_in = False
if 'merchantnumber' not in st.session_state:
  st.session_state.merchantnumber = ""
#Function to handle login
def login():
  st.session_state.logged_in = True
  st.session_state.merchantnumber = st.session_state.input_merchant_number
  #Function to handle logout
def logout():
  st.session_state.logged_in = False
  st.session_state.merchantnumber
#If Logged in, show a welcome message and logout button
if st.session_state.logged_in:
  st.write(f"Welcome Merchant, {st.session_state.merchantnumber}!*")
if st.button("Logout"):
  logout()
  st.experimental_rerun() # Refresh the app
else:
#If not logged in, show the login form
  st.write("Please enter your merchantnumber to log in.")
  st.session_state.input_merchant_number = st.text_input("username (Merchant Number)")
  st.text_input("Password", type='password')
  if st.button("Login"):
    if st.session_state.input_merchant_number: #Check if merchantnumber is provided
      login()
      st.session_state['current_page']='Gen AI'
      st.session_state['current_query'] = "SELECT FROM BI. Transactions WHERE CardSchemeCode = 'MC' AND Merchant Number 3286008088292144
      st.switch_page("pages/01_Home.py")
    else:
      st.error("Please enter a merchantnumber.")
