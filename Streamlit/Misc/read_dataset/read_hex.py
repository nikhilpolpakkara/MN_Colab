from pya2l import DB
import pya2l.model as model
import os
import pandas as pd

db = DB()
hex_file_path = "../../data/hex_a2l/bosch/JE351454010381.hex"
hex_file_path = os.path.abspath(hex_file_path)
a2l_file_path = '../../data/hex_a2l/bosch/MSE2_BJ10_0038_00.a2l'
a2l_file_path = os.path.abspath(a2l_file_path)
# path = r"D:\02_WORK\BAJAJ\POC\MN_Colab\Streamlit\data\hex_a2l\bosch\MSE2_BJ10_0038_00.a2l"
try:
    session = db.import_a2l(a2l_file_path, encoding="latin-1")
    session = db.open_existing("MSE2_BJ10_0038_00")
except:
    session = db.open_existing("MSE2_BJ10_0038_00")
# measurements = session.query(model.Measurement).order_by(model.Measurement.name).all()
# measurements = session.query(model.Characteristic).order_by(model.Characteristic.name).all()
# measurements = session.query(model.).order_by(model.SystemConstant.name).all()


def parse_intel_hex_line(line):
    line = line.strip()
    if not line.startswith(':'):
        return None  # Not a valid Intel HEX line

    byte_count = int(line[1:3], 16)  # Get byte count
    address = int(line[3:7], 16)  # Get address
    record_type = int(line[7:9], 16)  # Get record type
    data = [int(line[i:i + 2], 16) for i in range(9, len(line) - 2, 2)]  # Get data bytes
    checksum = int(line[-2:], 16)  # Get checksum

    return {
        'byte_count': byte_count,
        'address': address,
        'record_type': record_type,
        'data': data,
        'checksum': checksum
    }


def read_intel_hex_file(file_path):
    records = []

    with open(file_path, 'r') as file:
        for line in file:
            record = parse_intel_hex_line(line)
            if record:
                records.append(record)

    return records

def get_list_length(lst):
    return len(lst)

# Replace 'your_hex_file.hex' with the path to your actual hex file
hex_records = read_intel_hex_file(hex_file_path)
df = pd.DataFrame(hex_records)
print("OK")