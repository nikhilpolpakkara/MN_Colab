import intelhex
hex_file_path = "../../data/hex_a2l/bosch/JE351454010381.hex"
hex_file = intelhex.IntelHex(hex_file_path)
a = hex_file.todict()