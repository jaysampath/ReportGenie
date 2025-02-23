import os
import re
import openai
import streamlit as st
from datetime import datetime
from streamlit.logger import get_logger
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import Chatollama
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
import uuid
import requests
import json
import pandas as pd
Logger = get_logger('Langchain-Chatbot')
os.environ['OPENAI_API_KEY']=''
DATABRICKS_TOKEN = ''
#decorator
def enable_chat_history(func):
  if os.environ.get("OPENAI_API_KEY"):
    #to clear chat history after swtching chatbot
    current_page = func.__qualname__
    if "current page" not in st.session_state:
      st.session_state["current_page"] = current_page
    if st.session_state["current_page"] != current_page:
      try:
        st.cache_resource.clear()
        del st.session_state["current_page"]
        del st.session_state["messages"]
      except:
        pass
    # to show chat history on vi
    if "messages" not in st.session_state:
      st.session_state ["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    for msg in st.session_state["messages"]:
      if "dataframe" in msg:
        results_df= pd.DataFrame.from_records( data=msg["dataframe"], columns = msg["col_names"] ) 
        st.chat_message(msg["role"]).dataframe (results_df)
      if "button" in msg:
        st.chat_message(msg["role"]).button(msg["button"], on_click=msg["on_click"], args=msg["args"], disabled= msg["disabled"])
      if "code" in msg:
        st.chat_message(msg["role"]).code(msg["code"])
      if "content" in msg:
        st.chat_message(msg["role"]).write(msg["content"])
      if "json" in msg: 
        st.chat_message(msg["role"]).json(msg["json"])
  def execute(*args, **kwargs):
    func(*args, **kwargs)
    return execute
def display_msg(msg, author):
  """Method to display message on the UI
  Args:
  msg (str): message to display author (str): author of the message user/assistant """
  st.session_state.messages.append({"role": author, "content": msg})
  st.chat_message(author).write(msg)
def choose_custom_openai_key():
  openai_api_key = st.sidebar.text_input(label="OpenAI ΑΡΙ Key", type="password", placeholder="sk-... ", 
                                         key="SELECTED_OPENAI_API_KEY" )
  if not openai_api_key:
    st.error("Please add your OpenAI API key to continue.")
    st.info("Obtain your key from this link: https://platform.openai.com/account/api-keys") 
    st.stop()
  model ="gpt-40-mini"
  try:
    client = openai. OpenAI(api_key=openai_api_key)
    available_models = [{"id": i.id, "created": datetime.fromtimestamp(i.created)} for i in client.models.list() if str(i.id).startswith("gpt")]
    available_models = sorted (available_models, key=lambda x: x["created"])
    available_models = [i["id"] for i in available_models]
    model = st.sidebar.selectbox(
             label="Model",
             options = available_models,
             key="SELECTED_OPENAI_MODEL")
  except openai. AuthenticationError as e:
    st.error(e.body ["message"])
    st.stop()
  except Exception as e:
    print(e)
    st.error("Something went wrong. Please try again later.")
    st.stop()
  return model, openai_api_key
def configure_llm():
  llm = ChatOpenAI(model_name="databricks-meta-llama-3-1-70b-instruct", base_url="base_url", api_key=DATABRICKS_TOKEN)
  return llm
def print_qa(cls, question, answer):
  log_str = "\nUsecase: {}\nQuestion: {}\nAnswer: {}\n" +"-----"*10
  logger.info(log_str.format(cls._name, question, answer))
@st.cache_resource
def configure_embedding_model():
  embedding_model = FastEmbedEmbeddings(model_name="BAAI/bge-small-on-v1.5")
  return embedding_model
def sync_st_session():
  for k, v in st.session_state.items():
      st.session_state[k] = v
def get_template():
  return """
    You are an Al agent who's job is to write the correct SQL for my analysis. For the given input question and schema,
    ### Instruction:
    First four letters of a. Merchant Number is called a BIN. A partner can have multiple BINS.
    A Merchant can query MerchantTransactions, MerchantChargebacks, MerchantFunding tables. Understand the table columns. Ge
    ### question:
    {question}
    ### schema: {schema}
    ### output should be exactly in the below json format:
    {{
    "query": string
    }}
  
  """
def generate_report(query):
  #logic to generate a report
  pass
  
def create_report_subscription(query):
  #logic to create subscription
  pass