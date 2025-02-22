import utils
from streaming import StreamHandler
import streamlit as st
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_ollama.llms import OllamaLLM
os.environ ['HF_TOKEN']="hf_0jjkTVBeuQLmAKcLhkPHLdqYIashoLubGx"
os.environ['HUGGINGFACEHUB_API_TOKEN']="hf_0jjkTVBeuQLmAKcLhkPHLdqYIashoLubGx"
st.set_page_config(page_title="AI Reports Generator using Local LLM", page_icon="")
st.title("AI Reports Generator using Local LLM")
st.write("Generate reports using prompts")
class ReportingChatBot:
  def __init__(self):
    utils.sync_st_session()
    self.llm = OllamaLLM(model="llama3.1")
  @st.chache_resource
  def setup_chain(_self):
    memory = ConversationBufferMemory()
    chain = ConversationChain(llm=_self.llm, memory=memory, verbose=False)
    return chain
  @utils.enable_chat_history
  def main(self):
    chain = self.setup_chain()
    user_query = st.chat_input(placeholder="Enter your prompt here!")
    if user_query:
      utils.display_msg(user_query, 'user')
      with st.chat_message("assistant"):
        st_cb = StreamHandler(st.empty())
        result = chain.invoke( {"input":user_query}, {"callbacks": [st_cb]} )
        response = result["response"]
        st.session_state.messages.append({"role": "assistant", "content": response})
        utils.print_qa(ReportingChatBot, user_query, response)

if __name__ == "__main__":
  obj = ReportingChatBot()
  obj.main()
