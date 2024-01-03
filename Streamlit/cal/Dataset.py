from openpyxl import load_workbook
import numpy as np
from DBOps import ExcelOps, MongoDBOps
from DataTools import StringTools, DfTools
from pymongo import MongoClient


class ExcelDataset:
    def __init__(self, excel_file_path):
        self.excel_file_path = excel_file_path
        self.dataset_name = StringTools.get_file_name_without_extension(self.excel_file_path)
        self.wb = load_workbook(excel_file_path)
        self.svp_ws = self.wb["SVP"]
        self.maps_ws = self.wb["MAPS"]
        self.curves_ws = self.wb["CURVES"]
        self.svp_df = None
        self.client = None
        self.datahandler = None

    def load_svp_df(self):
        ref = self.svp_ws.tables["SVP"].ref
        self.svp_df = ExcelOps.get_df_from_cell_reference(sheet=self.svp_ws, ref=ref)

    def get_svp_documents(self):
        df = self.svp_df
        df = df.rename(columns={"NAME": "name", "VALUE": "value"})
        df["function"] = ""
        df["sub_function"] = ""
        df["category"] = ""
        df["variable_type"] = "SVP"
        df['value'] = df['value'].apply(DfTools.convert_to_float_or_str)
        svp_documents = df.to_dict(orient="records")
        return svp_documents

    def get_map_document(self, map_name):
        map_table = self.maps_ws.tables[map_name]
        map_df = ExcelOps.get_df_from_cell_reference(self.maps_ws, map_table.ref)
        map_df = map_df.dropna()
        try:
            map_df.columns = map_df.columns.astype("float")
        except Exception as e:
            pass
        map_df.reset_index(inplace=True)
        map_df = map_df.melt(id_vars='index', var_name='y', value_name='value')
        map_df.columns = ["x", "y", "value"]
        doc = {
            "name": map_name,
            "value": map_df.to_dict(orient="records"),
            "function": "",
            "sub_function": "",
            "category": "",
            "variable_type": "MAP"
        }

        return doc

    def load_mongo_client(self, client):
        self.client = client
        self.datahandler = MongoDBOps.MongoDBHandler(client)
        self.datahandler.load_database("CAL")
        self.datahandler.load_collection("DATASETS")

    def check_dataset_document(self):
        dataset_list = self.datahandler.get_field_values_from_level_1_collection(
            field_names=["dataset_id"]
        )
        if self.dataset_name in dataset_list:
            # TODO: if the dataset already exists in the database
            return True
        else:
            doc = {
                "dataset_id": self.dataset_name,
                "hex_data": []
            }
            self.datahandler.add_document_to_collection(doc)
            return False

    def transfer_svp_to_mongodb(self):
        self.load_svp_df()
        self.datahandler.append_list_values_to_level_1_collection_list_field(
            document_filter={"dataset_id": self.dataset_name},
            field_to_update="hex_data",
            new_values=self.get_svp_documents()
        )

    def transfer_maps_to_mongodb(self):
        map_documents = []
        for map_name in self.maps_ws.tables:
            map_doc = self.get_map_document(map_name)
            map_documents.append(map_doc)

        self.datahandler.append_list_values_to_level_1_collection_list_field(
            document_filter={"dataset_id": self.dataset_name},
            field_to_update="hex_data",
            new_values=map_documents
        )


if __name__ == "__main__":
    dataset_excel_file_path = "../data/T400_5N_dataset_step120.xlsx"
    client = MongoClient("mongodb://localhost:27017")
    dataset = ExcelDataset(dataset_excel_file_path)
    dataset.load_mongo_client(client=client)
    if not dataset.check_dataset_document():
        dataset.transfer_svp_to_mongodb()
        dataset.transfer_maps_to_mongodb()