import numpy as np
import pandas as pd
csv_path = "../data/emission_csv/single_line_csv_etr_entry.csv"
df = pd.read_csv(csv_path)


def emission_category(row):
    if row["RESULT"] == "PASS":
        if row["worst%"] > 85:
            return "V3"
        elif row["worst%"] > 75:
            return "V2"
        else:
            return "V3"
    else:
        return np.NAN


df["worst%"] = df[["CO%", "HC%", "NOX%", "NMHC%"]].max(axis=1)
df['category'] = df.apply(emission_category, axis=1)
df = df.drop(["worst%"], axis=1)