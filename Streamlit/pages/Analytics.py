import streamlit as st
from pymongo import MongoClient
import Mongodb_querries


client = MongoClient("mongodb://localhost:27017/")
db = client["TNV"]
line_color = "#2a9df4"

department_details = db["department_details"]

analytics_expander = st.expander("ANALYTICS", expanded=True)

with analytics_expander:
    st.write("Analytics")

