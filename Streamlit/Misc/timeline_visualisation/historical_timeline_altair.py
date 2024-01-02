import streamlit as st
import pandas as pd
import altair as alt

# Sample data for historical timeline
data = {
    'Event': ['Event A', 'Event B', 'Event C', 'Event D'],
    'Date': ['2022-01-01', '2022-03-15', '2022-06-20', '2023-02-10']
}

df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])

# Create a simple Altair chart
chart = alt.Chart(df).mark_bar().encode(
    x='Date:T',
    y='Event',
    tooltip=['Event', 'Date']
).properties(
    width=600,
    height=200
)

# Streamlit app
st.title('Historical Timeline')

# Display the chart
st.altair_chart(chart, use_container_width=True)
