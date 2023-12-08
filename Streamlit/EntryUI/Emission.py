import streamlit as st
import datetime
from MongoDBOps import crud_operations

line_color = "#2a9df4"
def print_session_state():
    print(st.session_state)

def test_data_entry():
    st.selectbox("a", options=[1, 2, 3, 4], on_change=print_session_state)
    st.text_input("b")
    st.text_area("Description", key="sdfs")