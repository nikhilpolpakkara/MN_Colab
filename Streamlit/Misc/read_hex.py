from pya2l import DB
import pya2l.model as model

db = DB()
hex_file_path = r'D:\BAL Projects\00_data\DH111204010381.hex'
a2l_file_path = r'D:\BAL Projects\00_data\MSE2_BJ10_0038_00.a2l'
session = db.import_a2l(a2l_file_path)
session = db.open_existing("MSE2_BJ10_0038_00")
measurements = session.query(model.Measurement).order_by(model.Measurement.name).all()

