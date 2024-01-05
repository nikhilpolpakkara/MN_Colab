import pandas as pd
from openpyxl import load_workbook
from DBOps import ExcelOps, MongoDBOps
from DataTools import StringTools, DfTools
from pymongo import MongoClient
from DBOps import TxtOps


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
            print(e)
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

    def get_curve_document(self, curve_name):
        curve_table = self.curves_ws.tables[curve_name]
        curve_df = ExcelOps.get_df_from_cell_reference(self.curves_ws, curve_table.ref)
        curve_df = curve_df.dropna()
        try:
            curve_df.columns = curve_df.columns.astype("float")
        except Exception as e:
            print(e)
            pass
        curve_df = curve_df.melt(var_name='x', value_name='value')
        doc = {
            "name": curve_name,
            "value": curve_df.to_dict(orient="records"),
            "function": "",
            "sub_function": "",
            "category": "",
            "variable_type": "CURVE"
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

    def transfer_curves_to_mongodb(self):
        curve_documents = []
        for curve_name in self.curves_ws.tables:
            curve_doc = self.get_curve_document(curve_name)
            curve_documents.append(curve_doc)

        self.datahandler.append_list_values_to_level_1_collection_list_field(
            document_filter={"dataset_id": self.dataset_name},
            field_to_update="hex_data",
            new_values=curve_documents
        )


class MongoDBDataset:
    def __init__(self, dataset_id, client):
        self.dataset_id = dataset_id
        self.client = client
        self.handler = MongoDBOps.MongoDBHandler(client)
        self.handler.load_database("CAL")
        self.handler.load_collection("DATASETS")

    def get_variable(self, variable_name):
        dataset_filter = {"dataset_id": self.dataset_id}
        hex_data_field = "hex_data"
        variable_filter = {"field_name": "name", "field_value": variable_name}
        variable_doc = self.handler.get_document_from_level_2_collection(
            nested_array=hex_data_field,
            collection_filter=dataset_filter,
            array_document_filter=variable_filter
        )
        if variable_doc["variable_type"] == "MAP":
            variable_doc["value_df"] = pd.DataFrame(variable_doc["value"]).pivot(index="x", columns="y", values="value")
        elif variable_doc["variable_type"] == "CURVE":
            variable_doc["value_df"] = pd.DataFrame(variable_doc["value"])
        return variable_doc


class DCMdataset:
    def __init__(self, dcm_file_path, ems = "BOSCH"):
        self.dcm_path = dcm_file_path
        self.svp = []
        self.curve = []
        self.map = []
        self.ems = ems
        self.characteristic_identifier : dict

    def detect_ems(self):
        pass
    def get_characteristic_dcm_variables(self):
        """
        Variable names to identify and sort DCM
        :return:
        """
        if self.ems == "BOSCH":
            self.characteristic_identifier = {"map":"KENNFELD",
                                              "curve":"KENNLINIE",
                                              "grouped_map":"GRUPPENKENNFELD",
                                              "grouped_curve":"GRUPPENKENNLINIE",
                                              "svp":"FESTWERT"}

    def extract_curve(self, lines):
        stx_values = []
        wert_values = []

        for line in lines:
            if line.startswith("ST/X"):
                # Extract ST/X values and remove the word "ST/X"
                stx_line = line.replace("ST/X", "").strip()
                stx_values.extend(map(float, stx_line.split()))
            elif line.startswith("WERT"):
                # Extract WERT values and remove the word "WERT"
                wert_line = line.replace("WERT", "").strip()
                wert_values.extend(map(float, wert_line.split()))

        result_list = [{'x': x, 'value': value} for x, value in zip(stx_values, wert_values)]

        return result_list

    def extract_map(self, lines):
        current_map = []
        current_x_values = None
        current_y_values = None

        for line in lines:
            if line.startswith("ST/X"):
                current_x_values = list(map(float, line.replace("ST/X", "").strip().split()))
            elif line.startswith("ST/Y"):
                current_y_values = float(line.replace("ST/Y", "").strip())
            elif line.startswith("WERT"):
                wert_values = list(map(float, line.replace("WERT", "").strip().split()))

                if current_x_values and current_y_values is not None:
                    for x, value in zip(current_x_values, wert_values):
                        current_map.append({'x': x, 'y': current_y_values, 'value': value})

        return current_map
    def get_content(self):
        dcm_content = TxtOps.extract_content_from_txt(self.dcm_path)
        return dcm_content

    def get_functions(self):
        dcm_content = self.get_content()
        function_names = TxtOps.find_lines_between_keywords(dcm_content,"FUNKTIONEN", "END")
        return function_names

    def read_content(self):
        dcm_content = TxtOps.split_lines_by_end(self.get_content(),"END")[1:]
        for content in dcm_content:
            variable_data = {}
            variable_data['name'] = content[1].split()[1]
            variable_data['function_name'] = content[3].split()[1]
            if content[1].startswith(self.characteristic_identifier['svp']):
                variable_data['value'] = content[5].split()[1]
                self.svp.append(variable_data)
            elif content[1].startswith(self.characteristic_identifier['curve']) or \
                    content[1].startswith(self.characteristic_identifier['grouped_curve']):
                variable_data['data'] = self.extract_curve(content)
                self.curve.append(variable_data)
            elif content[1].startswith(self.characteristic_identifier['map']) or \
                    content[1].startswith(self.characteristic_identifier['grouped_map']):
                variable_data['data'] = self.extract_map(content)
                self.map.append(variable_data)


class CsvDataset:
    def __init__(self, dataset_csv_path):
        self.dataset_csv_path = dataset_csv_path

    def get_hex_data_old_method(self):
        ind_of_svp = []
        svp_names = []
        svp_functions = []
        svp_values = []
        rows_map1 = []
        rows_map2 = []
        rows_map3 = []
        columns_map1 = []
        columns_map2 = []
        columns_map3 = []
        ind_of_yaxis = []
        ind_of_xaxis = []
        name_of_maps = []
        ioy_map2 = []
        iox_map2 = []
        names_map2 = []
        functions_map2 = []
        ioy_map1 = []
        iox_map1 = []
        names_map1 = []
        functions_map1 = []
        names_map3 = []
        functions_map3 = []
        iom12 = []
        iom = []
        iom3 = []
        iof3 = []
        df_list_map1 = []
        df_list_map2 = []
        df_list_map3 = []
        df1 = pd.DataFrame()
        df2 = pd.DataFrame()
        iof = []
        ioc = []
        ioc_1 = []
        ioc_2 = []
        iox_c1 = []
        names_c1 = []
        functions_c1 = []
        names_c2 = []
        functions_c2 = []
        c1_values = []
        c1_x_values = []
        c2_values = []
        c2_x_values = []
        c1_grid_points = []
        c2_grid_points = []
        svp_names_list = []
        svp_values_list_one = []
        maps_names_list = []
        maps_values_list_one = []
        try:
            df = pd.read_csv(self.dataset_csv_path, low_memory=False, encoding='unicode_escape')
        except:
            df = pd.read_csv(self.dataset_csv_path)

        first_column = df[df.columns[0]]
        for i in range(len(first_column)):
            if first_column[i] == "Y_AXIS_PTS":
                ind_of_yaxis.append(i)
                ind_of_xaxis.append(i - 4)
            elif first_column[i] == "VALUE":
                ind_of_svp.append(i)
            elif first_column[i] == "FUNCTION":
                iof.append(i)
            elif first_column[i] == "CURVE":
                ioc.append(i)
                if pd.isnull(df.iloc[i, 1]):
                    ioc_1.append(i)
                    iox_c1.append(i + 7)
                else:
                    ioc_2.append(i)

        for i in range(len(ioc_1)):
            names_c1.append(df.iloc[ioc_1[i] - 2, 1])
            functions_c1.append(df.iloc[ioc_1[i] + 3, 2])
            values = df.iloc[ioc_1[i] + 1]
            values = [x for x in values if str(x) != 'nan']
            if pd.isnull(df.iloc[ioc_1[i] + 1, 0]):
                pass
            else:
                values.remove(values[0])

            for j in range(len(values)):
                values[j] = float(values[j])

            c1_values.append(values)
            c1_grid_points.append(len(values))
            x_axis_values = df.iloc[iox_c1[i]]
            x_axis_values = [x for x in x_axis_values if str(x) != 'nan']
            try:
                x_axis_values.remove(x_axis_values[0])
            except:
                pass
            if pd.isnull(df.iloc[iox_c1[i], 1]):
                pass
            else:
                x_axis_values.remove(x_axis_values[0])

            for j in range(len(x_axis_values)):
                try:
                    x_axis_values[j] = float(x_axis_values[j])
                except:
                    pass

            c1_x_values.append(x_axis_values)

        for i in range(len(ioc_2)):
            names_c2.append(df.iloc[ioc_2[i] - 2, 1])
            functions_c2.append(df.iloc[ioc_2[i] + 3, 2])
            values = df.iloc[ioc_2[i] + 1]
            values = [x for x in values if str(x) != 'nan']
            if pd.isnull(df.iloc[ioc_2[i] + 1, 0]):
                pass
            else:
                values.remove(values[0])

            for j in range(len(values)):
                values[j] = float(values[j])

            c2_values.append(values)
            c2_grid_points.append(len(values))

            x_axis_values = df.iloc[ioc_2[i]]
            x_axis_values = [x for x in x_axis_values if str(x) != 'nan']
            x_axis_values.remove(x_axis_values[0])
            x_axis_values.remove(x_axis_values[0])

            for j in range(len(x_axis_values)):
                try:
                    x_axis_values[j] = float(x_axis_values[j])
                except:
                    pass

            c2_x_values.append(x_axis_values)

        names_curves = names_c1 + names_c2

        for i in range(len(ind_of_yaxis)):
            name_of_maps.append(df.iloc[ind_of_yaxis[i] - 2, 1])

        for i in range(len(ind_of_svp)):
            svp_names.append(df.iloc[ind_of_svp[i] - 2, 1])
            svp_functions.append(df.iloc[ind_of_svp[i] + 2, 2])

        for i in range(len(ind_of_svp)):
            svp_values.append(df.iloc[ind_of_svp[i], 2])

        for i in range(len(ind_of_yaxis)):
            if df.iloc[ind_of_yaxis[i] - 9, 0] == "FUNCTION":
                ioy_map2.append(ind_of_yaxis[i])
                iox_map2.append(ind_of_yaxis[i] - 4)
                names_map2.append(name_of_maps[i])
                functions_map2.append(df.iloc[ind_of_yaxis[i] - 9, 2])

            else:
                ioy_map1.append(ind_of_yaxis[i])
                iox_map1.append(ind_of_yaxis[i] - 4)
                names_map1.append(name_of_maps[i])
                functions_map1.append(df.iloc[ind_of_yaxis[i] - 8, 2])

        def rc(a, b):
            for i in range(len(a)):
                no = df.iloc[a[i]]
                if pd.isnull(df.iloc[a[i], 1]):
                    no = [x for x in no if str(x) != 'nan']
                    n = len(no) - 1
                else:
                    no = [x for x in no if str(x) != 'nan']
                    n = len(no) - 2
                b.append(n)
            return b

        rows_map1 = rc(ioy_map1, rows_map1)
        columns_map1 = rc(iox_map1, columns_map1)
        rows_map2 = rc(ioy_map2, rows_map2)
        columns_map2 = rc(iox_map2, columns_map2)

        # to get index of map having mentioned there axis seperately
        for i in range(len(ioy_map2)):
            iom12.append(ioy_map2[i] - rows_map2[i] - 12)
        for i in range(len(ioy_map1)):
            iom12.append(ioy_map1[i] - rows_map1[i] - 11)

        # to get index of maps of all maps
        for i in range(len(first_column)):
            if first_column[i] == "MAP":
                iom.append(i)

        if len(ind_of_yaxis) != 0:
            iom3 = [x for x in iom if x not in iom12]
        else:
            iom3 = iom
        # to get names of map3
        for i in range(len(iom3)):
            names_map3.append(df.iloc[iom3[i] - 2, 1])
        if len(iof) != 0:
            # to get no of rows and columns of map3
            for i in range(len(iom3)):
                for j in range(iom3[i], iom3[i] + 50):
                    if first_column[j] == "FUNCTION":
                        iof3.append(j)
                        functions_map3.append(df.iloc[iof3[i], 2])
                        break
            for i in range(len(iom3)):
                n = iof3[i] - iom3[i]
                rows_map3.append(n - 2)

            for i in range(len(iom3)):
                no = df.iloc[iom3[i] + 2]
                no = [x for x in no if str(x) != 'nan']
                n = len(no)
                columns_map3.append(n)
        else:
            for i in range(len(iom3)):
                no = df.iloc[iom3[i] + 2]
                no = [x for x in no if str(x) != 'nan']
                n = len(no)
                columns_map3.append(n)

                for j in range(iom3[i] + 2, iom3[i] + 100):
                    if pd.isnull(df.iloc[j, 2]):
                        rows_map3.append(j - iom3[i] - 2)
                        break

        # to get dataframes of map1

        for i in range(len(columns_map1)):
            try:
                print("getting dataframe of  ", names_map1[i])
                cl = []
                x = []
                y = []
                cl.clear()
                df1.empty
                df2.empty
                x.clear()
                y.clear()
                for j in range(rows_map1[i]):
                    y.append(df.iloc[ioy_map1[i], 2+j])
                # y_labels_map1.append(y)

                for j in range(columns_map1[i]):
                    cl.append(j + 2)
                    x.append(df.iloc[ioy_map1[i] - 4, j + 2])
                    # try:
                    #     x.append(float(df.iloc[ioy_map1[i] - 4][j + 2]))
                    # except:
                    #     x.append(df.iloc[ioy_map1[i] - 4][j + 2])

                # x_labels_map1.append(x)
                # try:
                #     cols = [float(n) for n in x]
                # except:
                #     cols = x
                df1 = pd.read_csv(self.dataset_csv_path, names=x, usecols=cl, skiprows=ioy_map1[i] - rows_map1[i] - 8,
                                  nrows=rows_map1[i], low_memory=False, encoding='unicode_escape'
                                  )
                df2 = df1
                try:
                    index_values = pd.Series(y).astype("float64").round(2)
                except:
                    index_values = pd.Series(y)

                df2.insert(loc=0, column='Y', value=index_values)
                try:
                    df2 = df2.round(3)
                except:
                    pass
                try:
                    df2.columns = df2.columns.astype("float64")
                except:
                    pass
                df_list_map1.append(df2.set_index("Y"))
            except:
                df_list_map1.append(pd.DataFrame())

        # to get dataframes of map2
        for i in range(len(columns_map2)):
            try:
                print(" getting data frame of  ", names_map2[i])
                cl = []
                x = []
                y = []
                cl.clear()
                x.clear()
                y.clear()
                for j in range(rows_map2[i]):
                    y.append(df.iloc[ioy_map2[i], 2 + j])

                for j in range(columns_map2[i]):
                    cl.append(j + 2)
                    x.append(df.iloc[ioy_map2[i] - 4, j + 2])
                    # try:
                    #     x.append(float(df.iloc[ioy_map2[i] - 4][j + 2]))
                    # except:
                    #     x.append(df.iloc[ioy_map2[i] - 4][j + 2])

                # try:
                #     cols = [float(n) for n in x]
                # except:
                #     cols = x

                df1 = pd.read_csv(self.dataset_csv_path, names=x, usecols=cl, skiprows=ioy_map2[i] - rows_map2[i] - 9,
                                  nrows=rows_map2[i], low_memory=False, encoding='unicode_escape'
                                  )
                df2 = df1

                try:
                    index_values = pd.Series(y).astype("float64").round(2)
                except:
                    index_values = pd.Series(y)

                df2.insert(loc=0, column='Y', value=index_values)
                # df2.index.astype("float64")
                try:
                    df2 = df2.round(3)
                except:
                    pass
                try:
                    df2.columns = df2.columns.astype("float64")
                except:
                    pass

                df_list_map2.append(df2.set_index("Y"))
            except:
                df_list_map2.append(pd.DataFrame())

        # to get dataframes of map3
        for i in range(len(columns_map3)):
            try:
                print("getting dataframes of  ", names_map3[i])
                cl = []
                x = []
                y = []
                cl.clear()
                df1.empty

                for j in range(columns_map3[i]):
                    cl.append(j + 1)
                df1 = pd.read_csv(self.dataset_csv_path, usecols=cl, header=None, skiprows=iom3[i] + 2, nrows=rows_map3[i],
                                  low_memory=False, encoding='unicode_escape', index_col=0
                                  )
                df2 = df1
                df2.columns = df2.iloc[0]
                df2 = df2[1:]
                df2 = df2.reset_index()
                df2.rename(columns={df2.columns[0]: "Y"}, inplace=True)
                df2 = df2.set_index(df2.columns[0])
                try:
                    df2 = df2.round(3)
                except:
                    pass

                try:
                    df2.columns = df2.columns.astype("float64")
                except:
                    pass

                df_list_map3.append(df2)

            except:
                df_list_map3.append(pd.DataFrame())

        all_maps_name = names_map1 + names_map2 + names_map3
        all_maps_functions = functions_map1 + functions_map2 + functions_map3
        all_maps_df = df_list_map1 + df_list_map2 + df_list_map3
        all_map_rows = rows_map1 + rows_map2 + rows_map3

        all_curves = names_c1 + names_c2
        all_curves_functions = functions_c1 + functions_c2
        all_curves_xaxis = c1_x_values + c2_x_values
        all_curves_values = c1_values + c2_values

        all_curves_df = []
        for ind, curve in enumerate(all_curves):
            df = pd.DataFrame([all_curves_xaxis[ind], all_curves_values[ind]])
            df.insert(loc=0, column='X', value=["X", "Y"])
            df = df.set_index("X")
            df = df.round(4)
            try:
                df.columns = df.iloc[0].round(3)
            except:
                df.columns = df.iloc[0]

            df = df[1:]
            all_curves_df.append(df)

        svp_df = pd.DataFrame([svp_names, svp_values, svp_functions])
        svp_df = svp_df.T
        svp_df.columns = ["NAME", "VALUE", "FUNCTION"]

        all_data = {
            "map_names": all_maps_name,
            "map_dfs": all_maps_df,
            "map_functions": all_maps_functions,
            "curve_names": all_curves,
            "curve_dfs": all_curves_df,
            "curve_functions": all_curves_functions,
            "svp": svp_df

        }

        return all_data


def transfer_dataset_excel_to_mongodb():
    # client = MongoClient("mongodb://localhost:27017")
    dataset_excel_file_path = "../data/T400_5N_dataset_step120.xlsx",
    client = MongoClient("mongodb://10.11.10.9:27017/")
    dataset = ExcelDataset(dataset_excel_file_path)
    dataset.load_mongo_client(client=client)
    if not dataset.check_dataset_document():
        dataset.transfer_svp_to_mongodb()
        dataset.transfer_maps_to_mongodb()
        dataset.transfer_curves_to_mongodb()


def read_dataset_from_mongodb():
    client = MongoClient("mongodb://10.11.10.9:27017/")
    dataset = MongoDBDataset(dataset_id="T400_5N_dataset_step120", client=client)
    variable_doc = dataset.get_variable("FWFTBRTA")


def read_dataset_from_csv():
    csv_dataset = CsvDataset(dataset_csv_path="../data/T400_5N_dataset_step120.CSV")
    hex_data = csv_dataset.get_hex_data_old_method()
    hex_data = csv_dataset.rearrange_data_from_old_method(data_from_old_method=hex_data)


def read_dcm_content():
    file_path = r"D:\BAL Projects\01_Misc\MN_Colab\Streamlit\data\DCM_STEP2A_V2___FOR_3W.DCM"
    dcm_handler = DCMdataset(file_path)
    dcm_handler.get_characteristic_dcm_variables()
    dcm_handler.read_content()


if __name__ == "__main__":

    client = MongoClient("mongodb://10.11.10.9:27017/")

    # transfer_dataset_excel_to_mongodb()
    # read_dataset_from_mongodb()
    # read_dataset_from_csv()
    # read_dcm_content()


