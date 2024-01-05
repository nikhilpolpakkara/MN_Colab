import pandas as pd
from DBOps import TxtOps

file_path = r"D:\BAL Projects\01_Misc\MN_Colab\Streamlit\data\DCM_STEP2A_V2___FOR_3W.DCM"

with open(file_path, 'r') as file:
    lines = file.readlines()

# Function to extract the string 2 lines after the line starting with "END"
def extract_strings(lines):
    variables = []
    for i in range(len(lines) - 1):
        if lines[i].startswith("END"):
            dict_ = {}
            # If "END" is found, capture the string 2 lines after it
            try:
                dict_['name'] = lines[i + 2].strip().split()[1]
                dict_['function_name'] = lines[i + 4].strip().split()[1]
                if lines[i + 2].startswith("FESTWERT"):
                    if lines[i + 6].strip().startswith("WERT"):
                        dict_['value'] = lines[i + 6].strip().split()[1]
            except:
                pass
            variables.append(dict_)
    return variables

# output_strings = extract_strings(lines)

content = TxtOps.extract_content_from_txt(file_path)

def find_lines_between_keywords(lines, start_keyword, end_keyword):
    result = []
    inside_block = False

    for line in lines:
        if line.startswith(start_keyword):
            inside_block = True
            try:
                result.append(line.split()[1])
            except:
                pass
        elif inside_block:
            try:
                result.append(line.split()[1])
            except:
                pass
            if line.startswith(end_keyword):
                inside_block = False
                break  # Stop capturing lines when the end keyword is found

    return result

function_names = find_lines_between_keywords(content,"END", "END")

def read_lines_after_keyword(file_lines, keyword):
    # Find the index of the first line starting with "END"
    end_index = next((index for index, line in enumerate(file_lines) if line.startswith(keyword)), None)

    if end_index is not None:
        # Remove lines before the first "END" line
        file_lines = file_lines[end_index+1:]
        return file_lines

new_content = read_lines_after_keyword(content,"END")

def split_lines_by_end(lines):
    blocks = []
    current_block = []

    for line in lines:
        current_block.append(line.strip())
        if line.startswith("END"):
            blocks.append(current_block)
            current_block = []

    return blocks


with open(file_path, 'r') as file:
    file_lines = file.readlines()

# Split lines by "END"
end_blocks = split_lines_by_end(file_lines)

def extract_map(lines):
    result_list = []
    current_map = None
    current_x_values = None
    current_y_values = None

    for line in lines:
        if line.startswith("KENNFELD"):
            if current_map:
                result_list.append(current_map)
            current_map = []
        elif line.startswith("ST/X"):
            current_x_values = list(map(float, line.replace("ST/X", "").strip().split()))
        elif line.startswith("ST/Y"):
            current_y_values = float(line.replace("ST/Y", "").strip())
        elif line.startswith("WERT"):
            wert_values = list(map(float, line.replace("WERT", "").strip().split()))

            if current_x_values and current_y_values is not None:
                for x, value in zip(current_x_values, wert_values):
                    current_map.append({'x': x, 'y': current_y_values, 'value': value})


    # Add the last map if any
    if current_map:
        result_list.append(current_map)

    return result_list

# Example usage:
your_list = ['KENNFELD KFHSUVXF 8 8',
 'LANGNAME "Line of heater voltage setpoint for off time calculation for lambda sensor heating depending on exh. gas temp"',
 'FUNKTION HLS',
 'EINHEIT_X "kg/h"',
 'EINHEIT_Y "Grad C"',
 'EINHEIT_W "V"',
 'ST/X   5.0000000000000000   8.0000000000000000   12.0000000000000000   18.0000000000000000   25.0000000000000000   30.0000000000000000',
 'ST/X   35.0000000000000000   40.0000000000000000',
 'ST/Y   300.0000000000000000',
 'WERT   9.9753906249999993   9.9351562500000004   9.8949218749999996   9.8851562499999996   9.8753906249999996   9.8804687500000004',
 'WERT   8.4402343749999993   7.0000000000000000',
 'ST/Y   400.0000000000000000',
 'WERT   9.4394531250000000   9.3230468749999993   9.2062500000000007   8.7988281250000000   8.3910156249999996   7.9140625000000000',
 'WERT   7.1070312500000004   6.2999999999999998',
 'ST/Y   500.0000000000000000',
 'WERT   9.2898437499999993   9.1316406249999993   8.9730468749999996   8.6113281250000000   8.2496093750000004   7.7191406249999996',
 'WERT   7.0097656250000000   6.2999999999999998',
 'ST/Y   550.0000000000000000',
 'WERT   9.5757812500000004   9.5175781250000000   8.8562499999999993   8.5175781250000000   8.1789062500000007   7.6214843749999996',
 'WERT   6.9609375000000000   6.2999999999999998',
 'ST/Y   600.0000000000000000',
 'WERT   9.4402343749999993   9.4246093749999993   9.0226562500000007   8.423828125000000',   'WERT   8.1078124999999996   7.5238281249999996',
   'WERT   6.9121093750000000   6.2999999999999998',
   'ST/Y   675.0000000000000000',
   'WERT   9.2453125000000007   8.9378906249999996   8.7691406250000004   7.3628906250000004   7.0250000000000004   6.7019531250000002',
   'WERT   6.8144531250000000   5.3007812500000000',
   'ST/Y   750.0000000000000000',
   'WERT   8.6800781249999996   8.0988281250000007   8.0554687499999993   6.5976562500000000   5.9011718750000002   5.8796875000000002',
   'WERT   5.0906250000000002   4.3015625000000002',
   'ST/Y   800.0000000000000000',
   'WERT   7.6992187500000000   7.3273437499999998   7.1074218750000000   6.3910156249999996   5.5425781250000004   5.3953125000000002',
   'WERT   4.5152343750000004   3.6351562500000001',
   'END']

# Extract ST/X, ST/Y, and WERT values and convert to a list of dictionaries
result_list = extract_map(your_list)

# Print or process the result list
for entry in result_list:
    print(entry)

