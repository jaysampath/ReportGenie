import streamlit as st
import utils

class QueryApprove:
    def __init__(self):
        something = 'something'
    def approve_from_user(self):
        approve_button = st.button('Approve Query')
        if approve_button:
            return True
        else:
            return False