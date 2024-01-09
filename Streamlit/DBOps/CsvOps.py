import pandas as pd


def find_start_line(file_path, keyword):
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, 1):
            if keyword in line:
                return line_num


if __name__ == "__main__":
    csv_path = "../data/K403_A.CSV"
    start_line = find_start_line(csv_path, keyword="FUNCTION_HDR")
    df = pd.read_csv(csv_path, skiprows=start_line)