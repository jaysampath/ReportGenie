import streamlit as st
import pandas as pd
st.set_page_config(page_title="ReportGenie", page_icon="")
st.header('Saved Queries')
def display_saved_queries():
  if not st.session_state.query_history:
    st.write('No saved queries yet!')
  else:
    df = pd.DataFrame (st.session_state.query_history, columns=["query"])
    st.dataframe(df, use_container_width=True)
if __name__ == "__main__":
  if "logged_in" not in st.session_state:
    st.write('Please login in Home Page to continue.')
  elif st.session_state.logged_in == False:
    st.write('You need to login to continue using it. Please go to Home Page to login')
  else:
    display_saved_queries()
