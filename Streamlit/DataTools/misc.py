from datetime import datetime, timedelta
import random
import os


def generate_random_dates(start_date, end_date, time_frame):
    random_dates = [start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))
                    for _ in range(time_frame)]

    formatted_dates = [date.strftime("%d-%m-%Y %H:%M:%S") for date in random_dates]
    return formatted_dates


def copy_streamlit_file_to_location(uploaded_file, destination_path):
    with open(destination_path, "wb") as f:
        f.write(uploaded_file.read())
    return f"File successfully copied to {destination_path}"


def create_directory_along_path(directory):
    try:
        os.makedirs(directory, exist_ok=True)
        print(f"Directory '{directory}' created successfully.")
    except OSError as e:
        print(f"Error creating directory '{directory}': {e}")


