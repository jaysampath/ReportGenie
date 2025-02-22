import streamlit as st
def save_query_to_history (query):
  """ Save the given query to the session history.
  Args:
  query (str): The SQL query to save. """
  if 'query_history' not in st.session_state:
    st.session_state.query_history = []
  if query:
    st.session_state.query_history.append(query) #st.success(f"Query saved to history: (query}")
def display_history():
  #Display the saved query history.
  if 'query_history' not in st.session_state:
    st.session_state.query_history = []
  st.subheader("Response History")
  if st.session_state.query_history:
    for i, hist_query in enumerate (st.session_state.query_history, 1): st.write(f"{i}, {hist_query}")
  else:
    st.write("No queries saved yet.")
