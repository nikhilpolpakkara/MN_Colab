from datetime import datetime, timedelta
import random


def generate_random_dates(start_date, end_date, time_frame):
    random_dates = [start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))
                    for _ in range(time_frame)]

    formatted_dates = [date.strftime("%d-%m-%Y %H:%M:%S") for date in random_dates]
    return formatted_dates
