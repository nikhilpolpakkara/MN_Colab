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
    session = db.open_create("MSE2_BJ10_0038_00")