# LAN PATHS

class CalPaths:
    def __init__(self, mode="dev"):
        self.mode = mode
        self.cal_data_path = None
        self.h1_calibration_path = None
        self.cal_k17_path = None
        if mode == "dev":
            self.set_development_lan_paths()

    def set_local_paths(self):
        pass

    def set_production_paths(self):
        self.cal_data_path = r"\\10.20.6.42\cal-data"
        self.h1_calibration_path = r"\\10.20.4.180\rnd\Groups\TNV\4_H1_CALIBRATION"
        self.cal_k17_path = r"\\10.20.4.180\CAL_K17_Data"

    def set_development_lan_paths(self):
        self.cal_data_path = r"\\10.20.6.42\cal-data\01_FI_DAT_FILES_ONLY_COMPRESSED\20_StreamlitTesting\cal-data"
        self.h1_calibration_path = r"\\10.20.4.180\CAL_K17_Data\StreamlitTesting\4_H1_CALIBRATION"
        self.cal_k17_path = r"\\10.20.4.180\CAL_K17_Data\StreamlitTesting\CAL_K17_Data"
        pass
