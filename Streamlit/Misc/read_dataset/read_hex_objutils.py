import objutils
hex_file_path = "../../data/hex_a2l/bosch/JE351454010381.hex"

a = objutils.load("ihex", hex_file_path)
objutils.dump("srec", "mySRecFile.srec", a)

a.read()