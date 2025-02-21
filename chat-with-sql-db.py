import utils
import os
import sqlite3
import streamlit as st
from streamlit.logger import get_logger
from pathlib import Path

from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.agent_toolkits_sql.base import sql_agent
from langchain_community.agent_toolkits_sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

logger = get_logger('Langchain-Chatbot')
st.set_page_config(page_title="ChatSQL")
st.header('Chat with SQL Database')
st.write('Enable the chatbot to interact with a SQL database through simple, conversational commands.')
os.environ["DATABRICKS_HOST"] = ''
os.environ["DATABRICKS_TOKEN"] = ''
DATABRICKS_TOKEN = 's'