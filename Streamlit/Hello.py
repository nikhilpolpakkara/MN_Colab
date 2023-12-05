import st_pages
import streamlit as st
from st_pages import Page, show_pages, hide_pages

# st.set_page_config(
#     page_title="TNV",
#     page_icon="👋",
# )

show_pages(
    [
        Page("pages/DataEntry.py", "DATA ENTRY"),
        Page("pages/Analytics.py", "DATA ANALYTICS"),
    ]
)

hide_pages(
    [
        Page("pages/tyre_wear.py", name="tyre_wear"),
     ]
)
