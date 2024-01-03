from openpyxl import load_workbook



class ExcelDataset:
    def __init__(self, excel_file_path):
        self.wb = load_workbook(excel_file_path)
        self.svp_ws = self.wb["SVP"]
        self.maps_ws = self.wb["MAPS"]
        self.curves_ws = self.wb["CURVES"]
        self.svp_df = self.svp_ws.tables["SVP"]

    def svp(self):
        pass

    def load_svp_df(self):
        ref = self.svp_ws.tables["SVP"].ref


if __name__ == "__main__":
    dataset_excel_file_path = "../../data/T400_5N_dataset_step120.xlsx"
    dataset = ExcelDataset(dataset_excel_file_path)