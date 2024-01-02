import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
file = r"D:\BAL Projects\01_Misc\MN_Colab\Streamlit\data\emission_csv\single_line_csv_etr_entry.csv"

df = pd.read_csv(file)
df['VTC'] = df['VTC'].astype(str)
st.title("Test Activity Dashboard")

# Add an option for displaying data for all models
model_names = ["All Models"] + list(df["MODEL"].unique())
selected_model = st.sidebar.selectbox("Select Model Name:", model_names)

# Filtered Data
if selected_model == "All Models":
    filtered_data = df
else:
    filtered_data = df[df["MODEL"] == selected_model]

# Total Tests Completed
total_tests_completed = len(filtered_data)
tests_passed = len(filtered_data[filtered_data["RESULT"] == "PASS"])
tests_failed = len(filtered_data[filtered_data["RESULT"] == "FAIL"])


# Display Total Tests, Pass, and Fail in a block with multiple lines
c1, c2, c3 = st.columns(3)
c1.metric("Total Tests Completed", total_tests_completed)
c2.metric("Tests Passed", tests_passed)
c3.metric("Tests Failed", tests_failed)

#######################################################################
# Display Total Tests in Each Test Cell
# st.subheader("Total Tests in Each Test Cell:")
# total_tests_by_cell = filtered_data.groupby("VTC")["RESULT"].value_counts().unstack().fillna(0)
# colors = {'Pass': 'blue', 'Fail': 'red'}
#
# # Plotting
# fig = px.bar(total_tests_by_cell, barmode='stack', color_discrete_map=colors)
# st.plotly_chart(fig)
#-----------------------------------------------------------------------
# Display Total Tests in Each Test Cell
filtered_data["DATE"] = pd.to_datetime(filtered_data["DATE"], format='%d/%m/%Y')

end_date = max(filtered_data["DATE"])
start_date = end_date - timedelta(days=6)
filtered_data_last_7_days = filtered_data[(filtered_data["DATE"] >= start_date) & (filtered_data["DATE"] <= end_date)]

# Calculate total tests by model for the last 7 days
total_tests_by_model_last_7_days = filtered_data_last_7_days.groupby("MODEL")["RESULT"].value_counts().unstack().fillna(0)
colors = {'Pass': 'blue', 'Fail': 'red'}

# Plotting a horizontal bar chart
fig = px.bar(total_tests_by_model_last_7_days, orientation='h', barmode='stack', color_discrete_map=colors)
fig.update_layout( xaxis_tickangle=-45)  # Adjust the angle of x-axis tick labels
st.plotly_chart(fig)
#######################################################################

# Create a sunburst chart
st.subheader("Sunburst Chart for Pass/Fail and Category for Selected Model:")
fig_sunburst = px.sunburst(
    filtered_data,
    path=['EMS','RESULT','category', ],
    color='RESULT',
    title='Sunburst Chart',
    # color_discrete_map={'PASS': 'green', 'FAIL': 'red'}
)

st.plotly_chart(fig_sunburst)

# Select columns for boxplot
selected_columns = ["CO%", "HC%", "NMHC%", "NOX%"]
import numpy as np
data = pd.DataFrame({
    'CO%': np.random.randint(0, 150, 100),
    'HC%': np.random.randint(0, 150, 100),
    'NMHC%': np.random.randint(0, 150, 100),
    'NOX%': np.random.randint(0, 150, 100),
})

# Create a single boxplot with multiple traces
st.subheader("Combined Boxplot for Selected Model:")
fig_combined_boxplot = px.box()

for column in selected_columns:
    fig_combined_boxplot.add_trace(
        go.Box(y=filtered_data[column], name=f"{column}")
    )

# Set y-axis range
fig_combined_boxplot.update_yaxes(range=[0, 150])

# Customize layout
fig_combined_boxplot.update_layout(
    title=f"Combined Boxplot for {selected_model}",
    xaxis_title="Selected Columns",
    yaxis_title="Values",
)

# Display the combined boxplot
st.plotly_chart(fig_combined_boxplot)



# Keep only the recent 20 recordings
filtered_data_recent = filtered_data.tail(10)

# Convert "SN" to a categorical type for proper ordering on the x-axis
filtered_data_recent["Tests"] = pd.Categorical(np.arange(0,10))

# Plot the values of the selected columns as a line
st.subheader(f"Selected Emission Percentage Values Over Time for {selected_model}")
fig_line_chart = px.line(
    filtered_data_recent,
    x="Tests",
    y=selected_columns,
    title=f"Emission Percentage Values Over Time for {selected_model}",
    range_y=[0, 150],  # Set y-axis range
    hover_name="SN",
    line_shape='spline',
    markers=True,
    # animation_frame="SN"
)
st.plotly_chart(fig_line_chart)

# Convert DATE column to datetime object


# Keep only the last 10 days of data
end_date = max(filtered_data["DATE"])
start_date = end_date - timedelta(days=7)
filtered_data_last_10_days = filtered_data[(filtered_data["DATE"] >= start_date) & (filtered_data["DATE"] <= end_date)]
filtered_data_last_10_days['VTC'] = filtered_data_last_10_days['VTC'].astype(str)

# Plot VTC column-wise count for the last 10 days with PASS/FAIL included
st.subheader("VTC Column-wise Count for the Last Week:")
vtc_count_last_10_days = filtered_data_last_10_days.groupby(["VTC", "RESULT"]).size().reset_index(name='Count')

fig_bar_chart = px.bar(
    vtc_count_last_10_days,
    x="VTC",
    y="Count",
    color="RESULT",
    labels={"x": "VTC", "y": "Count", "color": "Result"},
    title="VTC Column-wise Count for the Last 10 Days with PASS/FAIL"
)
st.plotly_chart(fig_bar_chart)