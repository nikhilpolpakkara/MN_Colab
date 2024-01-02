try:
	import time
	import plotly.graph_objects as go
	from plotly.subplots import make_subplots
	from plotly.offline import plot
	import os
	from asammdf import MDF
	import statistics
	import pandas as pd
	import easygui
	import tkinter as tk
	import socket
	from datetime import datetime
	from datetime import date
	from tkinter.ttk import Progressbar
	from tkinter import *
	from tkinter.ttk import *

except:
	pass

import numpy as np
local = 1
etr_entry_mode = 1

print(f"local is {local} i.e. Application running on server")

no_internet_ip = ["10.11.9.112", "192.168.1.1", "10.11.8.101", "10.11.8.229"]

if local == 0:
    mdf_file_path = "//10.20.6.42/cal-data/01_FI_DAT_FILES_ONLY_COMPRESSED/4_ETR_2W_MDF/"
    dat_file_path_html = "//10.20.6.42/cal-data/01_FI_DAT_FILES_ONLY_COMPRESSED/1_ETR_2W/"
    run_details_csv = r"\\10.20.4.180\rnd\Groups\TNV\4_H1_CALIBRATION\17_ETR\CAL_ETR_&_Dataset_Application\DATA\07_logs\html_history.csv"
    etr_report_location = r"\\10.20.6.42\cal-data\01_FI_DAT_FILES_ONLY_COMPRESSED\16_ETR_REPORTS"
    single_line_csv_path = r"\\10.20.4.180\rnd\Groups\TNV\4_H1_CALIBRATION\17_ETR\CAL_ETR_&_Dataset_Application\DATA\01_2W\02_DATABASE\single_line_csv_etr_entry.csv"
else:
    mdf_file_path = "D:/BAL Projects/01_Misc/MN_Colab/Streamlit/data/mf4_files/"
    dat_file_path_html = "D:/BAL Projects/01_Misc/MN_Colab/Streamlit/data/dat_files/"
    single_line_csv_path = r"D:\BAL Projects\01_Misc\MN_Colab\Streamlit\data\emission_csv\single_line_csv_etr_entry.csv"

# etr_no_required = ["8900"]
# inca_variables_additional = []
# wmtc_class_list = []
remarks = ["", "", "", "", "", "", ""]
# ltheme = 0
# smooth = 0
# ecarb=0


def html_report(etr_no_required, inca_variables_additional, wmtc_class_list, remark_dict, remark_entries, ltheme, smooth, ecarb, vdpl, tid, call="etr_entry", unit="ppm"):

    start_time = time.time()
    all_mdf_files = os.listdir(mdf_file_path)
    all_dat_files = os.listdir(dat_file_path_html)

    available_mdf_files = []
    available_dat_files = []
    print("inside html report")
    for n in etr_no_required:
        for m in all_mdf_files:
            if "ETR" + str(n) in m:
                if m.endswith(".mf4"):
                    available_mdf_files.append(n)
                elif m.endswith(".zip"):
                    available_mdf_files.append(n)

        for d in all_dat_files:
            if "ETR" + str(n) in d:
                if d.endswith(".dat"):
                    available_dat_files.append(n)

    print("AVAILABLE MDF FILES ", available_mdf_files)
    print("AVAILABLE DAT FILES ", available_dat_files)

    ########################################################################################################################
    phases = {}
    phases["part1"] = {}
    phases["part2"] = {}
    phases["part3"] = {}
    phases["part1r"] = {}
    phases["part2r"] = {}
    phases["part3r"] = {}

    modes = ["idle", "acceleration", "cruise", "deceleration"]
    #phases are the breakdown of WMTC cycle in part1, part2 etc
    for i in phases.keys():
        for j in modes:
            phases[i][j] = {}

    ########################################################################################################################

    phases["part1r"]["idle"]["start"] = [0, 69, 151, 254, 402, 474, 515, 537, 588]
    phases["part1r"]["idle"]["end"] = [22, 74, 185, 267, 408, 486, 519, 542, 601]
    phases["part1r"]["acceleration"]["start"] = [22, 74, 134, 185, 267, 319, 408, 486, 503, 519, 542]
    phases["part1r"]["acceleration"]["end"] = [39, 91, 140, 203, 277, 327, 429, 499, 507, 528, 553]
    phases["part1r"]["cruise"]["start"] = [39, 91, 116, 203, 277, 327, 429, 456, 553]
    phases["part1r"]["cruise"]["end"] = [60, 110, 125, 242, 314, 392, 436, 463, 573]
    phases["part1r"]["deceleration"]["start"] = [60, 110, 125, 140, 242, 314, 392, 436, 463, 499, 528, 573]
    phases["part1r"]["deceleration"]["end"] = [69, 116, 134, 151, 254, 319, 402, 456, 474, 515, 537, 588]

    phases["part1"]["idle"]["start"] = [0, 69, 151, 254, 402, 474, 515, 537, 588]
    phases["part1"]["idle"]["end"] = [22, 74, 185, 267, 408, 486, 519, 542, 601]
    phases["part1"]["acceleration"]["start"] = [22, 74, 134, 183, 222, 267, 319, 408, 486, 503, 519, 542]
    phases["part1"]["acceleration"]["end"] = [39, 91, 140, 195, 227, 277, 327, 429, 499, 507, 528, 553]
    phases["part1"]["cruise"]["start"] = [39, 91, 116, 195, 277, 327, 429, 456, 553]
    phases["part1"]["cruise"]["end"] = [60, 110, 125, 214, 314, 392, 436, 463, 573]
    phases["part1"]["deceleration"]["start"] = [60, 110, 125, 140, 214, 227, 314, 392, 436, 463, 499, 528, 573]
    phases["part1"]["deceleration"]["end"] = [69, 116, 134, 151, 222, 319, 256, 402, 456, 474, 515, 537, 588]

    phases["part2"]["idle"]["start"] = [0, 69, 151, 254, 402, 474, 515, 537, 588]
    phases["part2"]["idle"]["end"] = [22, 74, 185, 267, 408, 486, 519, 542, 601]
    phases["part2"]["acceleration"]["start"] = [22, 74, 134, 185, 267, 319, 408, 486, 503, 519, 542]
    phases["part2"]["acceleration"]["end"] = [39, 91, 140, 203, 277, 327, 429, 499, 507, 528, 553]
    phases["part2"]["cruise"]["start"] = [39, 91, 116, 203, 277, 327, 429, 456, 553]
    phases["part2"]["cruise"]["end"] = [60, 110, 125, 242, 314, 392, 436, 463, 573]
    phases["part2"]["deceleration"]["start"] = [60, 110, 125, 140, 242, 314, 392, 436, 463, 499, 507, 528, 573]
    phases["part2"]["deceleration"]["end"] = [69, 116, 134, 151, 254, 319, 402, 456, 474, 503, 515, 537, 588]

    phases["part2r"]["idle"]["start"] = [0, 69, 151, 254, 402, 474, 515, 537, 588]
    phases["part2r"]["idle"]["end"] = [22, 74, 185, 267, 408, 486, 519, 542, 601]
    phases["part2r"]["acceleration"]["start"] = [22, 74, 134, 185, 267, 319, 408, 486, 503, 519, 542]
    phases["part2r"]["acceleration"]["end"] = [39, 91, 140, 203, 277, 327, 429, 499, 507, 528, 553]
    phases["part2r"]["cruise"]["start"] = [39, 91, 116, 203, 277, 327, 429, 456, 553]
    phases["part2r"]["cruise"]["end"] = [60, 110, 125, 242, 314, 392, 436, 463, 573]
    phases["part2r"]["deceleration"]["start"] = [60, 110, 125, 140, 242, 314, 392, 436, 463, 499, 507, 528, 573]
    phases["part2r"]["deceleration"]["end"] = [69, 116, 134, 151, 254, 319, 402, 456, 474, 503, 515, 537, 588]

    phases["part3"]["idle"]["start"] = [0, 69, 151, 256, 402, 474, 515, 537, 588]
    phases["part3"]["idle"]["end"] = [22, 74, 183, 267, 408, 486, 519, 542, 601]
    phases["part3"]["acceleration"]["start"] = [22, 74, 134, 183, 222, 267, 319, 408, 486, 503, 519, 542]
    phases["part3"]["acceleration"]["end"] = [39, 92, 140, 195, 227, 278, 327, 429, 499, 507, 527, 551]
    phases["part3"]["cruise"]["start"] = [39, 92, 116, 195, 278, 327, 429, 456, 551, ]
    phases["part3"]["cruise"]["end"] = [61, 111, 125, 214, 314, 392, 436, 463, 573]
    phases["part3"]["deceleration"]["start"] = [61, 111, 140, 214, 227, 314, 392, 436, 463, 507, 527, 573]
    phases["part3"]["deceleration"]["end"] = [69, 134, 151, 222, 256, 319, 402, 456, 503, 515, 537, 588]

    phases["part3r"]["idle"]["start"] = [0, 69, 151, 256, 402, 474, 515, 537, 588]
    phases["part3r"]["idle"]["end"] = [22, 74, 183, 267, 408, 486, 519, 542, 601]
    phases["part3r"]["acceleration"]["start"] = [22, 74, 134, 183, 222, 267, 319, 408, 486, 503, 519, 542]
    phases["part3r"]["acceleration"]["end"] = [39, 92, 140, 195, 227, 278, 327, 429, 499, 507, 527, 551]
    phases["part3r"]["cruise"]["start"] = [39, 92, 116, 195, 278, 327, 429, 456, 551, ]
    phases["part3r"]["cruise"]["end"] = [61, 111, 125, 214, 314, 392, 436, 463, 573]
    phases["part3r"]["deceleration"]["start"] = [61, 111, 140, 214, 227, 314, 392, 436, 463, 507, 527, 573]
    phases["part3r"]["deceleration"]["end"] = [69, 134, 151, 222, 256, 319, 402, 456, 503, 515, 537, 588]

    ########################################################################################################################

    classes = [10, 21, 22, 31, 32]
    class_breakdown = {}
    class_breakdown[10] = ["part1r", "part1"]
    class_breakdown[21] = ["part1r", "part2r"]
    class_breakdown[22] = ["part1", "part2"]
    class_breakdown[31] = ["part1", "part2", "part3r"]
    class_breakdown[32] = ["part1", "part2", "part3"]
    #each part/phase is divided into hills
    #for ecsh class phase1 hills are same
    #ohase2 hills for class 10 are different than rest others
    hills = ["P1H", "P2H", "P3H"]
    P1H = {}
    P2H = {}
    P3H = {}
    for i in classes:
        P1H[i] = {}
        P1H[i]["start"] = []
        P1H[i]["end"] = []

        P2H[i] = {}
        P2H[i]["start"] = []
        P2H[i]["end"] = []

        P3H[i] = {}
        P3H[i]["start"] = []
        P3H[i]["end"] = []

    for i in classes:
        P1H[i]["start"] = [1, 72, 186, 268, 408, 486, 516, 540]
        P1H[i]["end"] = [72, 186, 268, 408, 486, 516, 540, 601]

    P2H[10]["start"] = [601, 672, 786, 868, 1008, 1086, 1116, 1141]
    P2H[10]["end"] = [672, 786, 868, 1008, 1086, 1116, 1141, 1201]

    for i in range(1, len(classes)):
        P2H[classes[i]]["start"] = [601, 651, 742, 812, 911, 994, 1101]
        P2H[classes[i]]["end"] = [651, 742, 812, 911, 994, 1101, 1201]

    for i in range(3, len(classes)):
        P3H[classes[i]]["start"] = [1201, 1321, 1386, 1521, 1566]
        P3H[classes[i]]["end"] = [1321, 1386, 1521, 1566, 1800]

    ########################################################################################################################
    # TO GET MODAL DATA
    modal_variables = ["Speed", "HC_g/s", "CO_g/s", "NOx_g/s", "HC_ppm", "CO_ppm", "NOx_ppm"]

    modal_df_list = {}
    for n in etr_no_required:
        modal_df_list[n] = pd.DataFrame()

    for n in etr_no_required:
        found = 0
        if n in available_mdf_files:
            try:
                found = 1
                print("COLLECTING MDF DATA FOR ETR NO ", n)
                mdf_file = MDF(mdf_file_path + "ETR" + str(n) + ".mf4")
                mdf_df = mdf_file.to_dataframe(channels=modal_variables, empty_channels="skip", use_display_names=True)
                mdf_df = mdf_df.reset_index()
                mdf_df.timestamps = pd.to_timedelta(mdf_df.timestamps*1000000000)
                mdf_df.set_index("timestamps", inplace=True)
                mdf_df = mdf_df.resample("1s").mean()
                mdf_df = mdf_df.reset_index()
                modal_df_list[n] = mdf_df
            except:
                modal_df_list[n] = pd.DataFrame(columns=modal_variables)

        if found == 0:
            modal_df_list[n] = pd.DataFrame(columns=modal_variables)

    ##################################
    # GETTING CLASS BASED ON MAX SPEED
    # determining class based on modal that because basis that we will trim the dat file to 1200 or 1800 seconds
    # csv_df = pd.read_csv(single_line_csv_path,  low_memory=False, encoding='unicode_escape')
    csv_df = pd.read_csv(single_line_csv_path)

    for n in etr_no_required:
        try:
            max_speed = max(modal_df_list[n]["Speed"])
            print(n, " ", "MAX SPEED = ", max_speed)
            if 45 <= max_speed <= 55:
                wmtc_class_list.append(10)
            elif 75 <= max_speed <= 87:
                wmtc_class_list.append(21)
            elif 90 <= max_speed <= 100:
                wmtc_class_list.append(22)
            elif 105 <= max_speed <= 115:
                wmtc_class_list.append(31)
            elif 115 <= max_speed <= 130:
                wmtc_class_list.append(31)

        except:
            try:
                wmtc_class_list.append(int(csv_df[csv_df.SN == n].iloc[-1].CL))
            except:
                c = easygui.enterbox(" ", "please enter class of " + str(n))
                wmtc_class_list.append(int(c))
        print("CLASS", wmtc_class_list)

    print("DETECTING EMS SYSTEM")
    ecarb = 0
    vdpl = 0
    bosch = 0
    mikuni = 0
    dat_file_path = dat_file_path_html + "/ETR" + str(etr_no_required[0]) + ".dat"
    if os.path.isfile(dat_file_path):

        try:
            dat_file = MDF(dat_file_path)
            try:
                dat_file.get("RPM")
                vdpl = 1
                print("VDPL EMS")
            except:
                try:
                    dat_file.get("cps_n_engine")
                    ecarb = 1
                    print("ECARB EMS")
                except:
                    try:
                        dat_file.get("nmot_w")
                        bosch = 1
                        print("BOSCH EMS")
                    except:
                        try:
                            dat_file.get("g_Crnk_Rev")
                            mikuni = 1
                            print("MIKUNI EMS")
                        except:
                            print("UNABLE TO IDENTIFY EMS")

        except:
            print("THERE WAS SOME ERROR IN READING DAT FILE FOR DETECTING EMS")
    else:
        print("DAT FILE DOES NOT EXIST")

    ########################################################################################################################
    # TO GET INCA DATA
    if bosch == 1:
        inca_variables = ["nmot_w",
                  "olls_w",
                  "wdkba_w",
                  "fr_w", "lamsol",
                  "zwout",
                  "rka_w", "fra_w", "ofmsdkq_w", "fkmsdk_w",
                   "dmllri_w",
                  "dmvad_w",
                  "tateout_w",
                  "pu", "psxzs_w",
                  'fkpvdk_w',
                  'rkte_w',
                  "tans", "tmot"
                  ]
    elif vdpl == 1:
        inca_variables = ["RPM",
                            "IACV",
                            "TPS",
                            "CLC","lamsol",
                            "COILADV1",
                            "COILADV2", "AF_FUELOFFSET", "INJQUANT1",
                            "STATICFUELCOMP",
                            "EWTFUELCOMP",
                            "EWTADVCOMP",
                            "LAMBDAV1",
                            "MAP", "BARO",
                            "EVAP_FLOW",
                            "MILFAULT",
                            "EWT", "MAT",

                            "SLOWIACVI",
                            "VBATT",

                            ]
    elif mikuni == 1:
        inca_variables = ["g_Crnk_Rev",
                          "g_Ac2drive_CurPos",
                          "g_Thp_Val",
                          "g_O2fb_Cps", "","g_Ign_Tmg","g_FuelWt_Cps",
                          "g_Iprs_PRat", "g_Aprs_Val", "g_Acdc_Cps",
                          "g_Dcfcut_Cps", "g_Wt_Val", "g_At_Val",
                          "l_Fuel_Rat"]

    elif ecarb == 1:
        inca_variables = ["cps_n_engine",
                                            "ecarb_pct_solenoid_PWM",
                                            "tps_pct_throttle_position",
                                            "ecarb_U_lm_sensor_signal",
                                            "ecarb_v_vehicle_speed",
                                            "ecarb_deg_primary_ign",
                                            "ecarb_pct_take_off_PWM",
                                            "ecarb_b_orc_condition",
                                            "ecarb_sv_control_state",
                                            "afm_b_mil_active",
                                            "afm_b_vss_fault_active",
                                            "ecarb_b_idle_control_active",
                                            "cps_cnt_pip_reset_fault",
                                            "ecarb_T_engine_temp",
                                            "tps_U_sensor",
                                            "ecarb_pct_warmup_PWM",
                                            "ecarb_deg_secondary_ign",
                                            ]
    else:
        inca_variables = [" ",
                          " ",
                          " ",
                          " ", " ",
                          " ",
                          " ", " ", " ", " ",
                          " ",
                          " ",
                          " ",
                          " ", " ",
                          ' ',
                          ' ',
                          " ", " "
                          ]


    error_names = ["DFES_numDFC_[0]",
                   "DFES_numDFC_[1]",
                   "DFES_numDFC_[2]",
                   "DFES_numDFC_[3]",
                   "DFES_numDFC_[4]"] if ecarb == 0 else ["afm_b_mil_active", "afm_b_vss_fault_active"]

    error_status = ["DFES_stChk_[0]",
                    "DFES_stChk_[1]",
                    "DFES_stChk_[2]",
                    "DFES_stChk_[3]",
                    "DFES_stChk_[4]"] if ecarb == 0 else ["afm_b_mil_active", "afm_b_vss_fault_active"]

    error_df_list = {}
    inca_df_list = {}
    start_row = {}
    end_row = {}
    #initializing with empty data which will be filled later
    for n in range(len(etr_no_required)):
        inca_df_list[etr_no_required[n]] = pd.DataFrame()
        error_df_list[etr_no_required[n]] = pd.DataFrame()
        start_row[etr_no_required[n]] = 0
        end_row[etr_no_required[n]] = 1200 if wmtc_class_list[n] < 30 else 1800 #to be checked

    counter = 0
    for n in etr_no_required:
        found = 0
        if n in available_dat_files:
            found = 1
            print("COLLECTING DAT DATA FOR ETR NO ", n)
            dat_file = MDF(dat_file_path_html + "ETR" + str(n) + ".dat")
            all_channels = list(dat_file.channels_db)
            try:
                error_df = dat_file.to_dataframe(channels=error_names + error_status if ecarb == 0 else error_names, raster=1,
                                                    empty_channels="skip", use_display_names=True)  #this will create a df even if some signals are missing it will create df of availaible channels
                common_signals = list(set(error_names + error_status).intersection(list(all_channels))) #but that will have XCP CCP in its name so we will have to rename the df columns

                for i in error_df.columns:
                    error_df = error_df.rename(columns={i: i.split("\\")[0]}, inplace=False)

                channels_not_available = list(set(error_names + error_status) - set(common_signals))  #the channels which are not available appending NA in place of that
                for i in channels_not_available:
                    error_df[i] = "NA"
                error_df = error_df[error_names + error_status]
                error_df_list[n] = error_df

            except:
                error_df_list[n] = pd.DataFrame(error_names + error_status)
                print(n, "ERROR IN COLLECTING ERROR HISTORY DATA")
                pass

            try:
                common_signals = list(set(inca_variables + inca_variables_additional).intersection(list(all_channels)))
                df = dat_file.to_dataframe(channels=common_signals,
                                           use_display_names=True, ignore_value2text_conversions=True)
                for i in df.columns:
                    df = df.rename(columns={i: i.split("\\")[0]}, inplace=False)

                channels_not_available = list(set(inca_variables + inca_variables_additional) - set(common_signals))
                for i in channels_not_available:
                    df[i] = 0

                df1 = df.reset_index()
                df1.timestamps = pd.to_timedelta(df1.timestamps * 1000000000)
                df1.set_index("timestamps", inplace=True)
                df1 = df1.resample("1s").mean()
                df1 = df1.reset_index()

                if mikuni == 1:
                    nmot = df1["g_Crnk_Rev"].to_list()

                elif ecarb == 0:
                    if vdpl == 0:
                        nmot = df1["nmot_w"].to_list()
                    else:
                        nmot = df1["RPM"].to_list()
                else:
                    nmot = df1["cps_n_engine"].to_list()

                for i in range(len(nmot)):
                    if nmot[i] > 0:
                        start_row[n] = i
                        end_row[n] = 1200 + i if wmtc_class_list[0] < 30 else 1800 + i
                        print(len(nmot) - start_row[n])
                        break

                inca_df_list[n] = df1

            except:
                inca_df_list[n] = pd.DataFrame(columns=inca_variables)
                print("THERE WAS SOME ERROR IN INCA DATA COLLECTION")

        if found == 0:
            inca_df_list[n] = pd.DataFrame(columns=inca_variables)
            error_df_list[n] = pd.DataFrame(columns=error_names + error_status)


    ########################################################################################################################
    # TO GET PHASES OF THE CLASS
    parts = {}
    for n in range(len(etr_no_required)):
        parts[etr_no_required[n]] = []
        wmtc_class = wmtc_class_list[n]
        for i in class_breakdown.keys():
            if wmtc_class == i:
                parts[etr_no_required[n]] = class_breakdown[i]


    ########################################################################################################################
    # CALCULATING EMISSION RESULTS MODAL DATA
    # this section is available in ETR REPORT 1.5

    ########################################################################################################################
    fixed_layout = [
        [{"type": "Table", "colspan": 2, "rowspan": 2}, {"type": "Table"}],
        [{"type": "xy", "rowspan": 2, "secondary_y": True}, {}],
        [{"type": "xy", "rowspan": 2, "secondary_y": True}, {}],
        [{"type": "xy", "rowspan": 2, "secondary_y": True}, {}],
        [{"type": "xy", "rowspan": 2, "secondary_y": True}, {}],
        [{"type": "xy", "rowspan": 2, "secondary_y": True}, {}],
        [{"type": "xy", "rowspan": 2, "secondary_y": True}, {}],
        [{"type": "xy", "secondary_y": True}, {}],
        [{"type": "xy", "secondary_y": True}, {}],
        [{"type": "xy", "secondary_y": True}, {}],
        [{"type": "xy", "secondary_y": True}, {}],
        [{"type": "xy", "secondary_y": True}, {}],
        [{"type": "xy", "secondary_y": True}, {}],
        [{"type": "xy", "secondary_y": True}, {}],#till here dependent inca signals
        [{"type": "xy", "secondary_y": True}, {"type": "Table", "rowspan": 2}],
        [{"type": "xy", "secondary_y": True}, {"type": "Table"}],
        [{"type": "xy", "secondary_y": True}, {"type": "Table", "rowspan": 2}],
        [{"type": "xy", "secondary_y": True}, {"type": "Table"}],
        [{"type": "xy", "secondary_y": True}, {"type": "Table", "rowspan": 2}],
        [{"type": "xy", "secondary_y": True}, {"type": "Table"}],
        [{"type": "xy", "secondary_y": True}, {}],
        [{"type": "xy", "secondary_y": True}, {"type": "Table", "rowspan": 3}],
        [{"type": "xy", "secondary_y": True}, {"type": "Table"}],
        [{"type": "xy", "secondary_y": True}, {"type": "Table"}]
    ]
    #fixed_layout = np.array(fixed_layout).reshape(21, 2)

    if mikuni == 1:
        fixed_layout_titles = [
            "", "",
            "", "",
            f"HC({unit})", "HC Hill wise",
            "", "HC Hill wise  cumulative",
            f"CO({unit})", "CO Hill wise",
            "", "CO Hill wise  cumulative",
            f"NOx({unit})", "NOx Hill wise",
            "", "NOx Hill wise cumulative",
            "SPEED", "HC Mode wise",
            "RPM", "CO Mode wise",
            "Stepper opening", "NOx Mode wise",
            "Throttle opening", "Throttle opening hill wise",
            "g_O2fb_Cps", "FR Mode wise",
            "g_Ign_Tmg", "Primary Ign Timing",
            "g_FuelWt_Cps", "WMTC START DATA",
            "g_Iprs_PRat", "",
            "g_Aprs_Val", "WMTC END DATA",
            "g_Acdc_Cps", "",
            "g_Dcfcut_Cps", "WMTC MIN MAX DATA",
            "g_Wt_Val", "",
            "g_At_Val", "ERROR History",
            "l_Fuel_Rat", "",
        ]

    elif ecarb == 0:
        if vdpl == 0:
            fixed_layout_titles = [
        "", "",
        "", "",
        f"HC({unit})", "HC Hill wise",
        "", "HC Hill wise  cumulative",
        f"CO({unit})", "CO Hill wise",
        "", "CO Hill wise  cumulative",
        f"NOx({unit})", "NOx Hill wise",
        "", "NOx Hill wise cumulative",
        "SPEED", "HC Mode wise",
        "RPM", "CO Mode wise",
        "Stepper opening", "NOx Mode wise",
        "Throttle opening", "Throttle opening hill wise",
        "fr", "FR Mode wise",
        "zwout", "Primary Ign Timing",
        "rka", "WMTC START DATA",
        "fra", "",
        "leakage", "WMTC END DATA",
        "fkmsdk", "",
        "dmllri", "WMTC MIN MAX DATA",
        "dmvad", "",
        "tateout_w", "",
        "pu & Manifold air pressure", "ERROR History",
        "fkpvdk_w", "",
        "rkte_w", ""
    ]
        else:
            fixed_layout_titles = [
                 "", "",
        "", "",
        f"HC({unit})" , "HC Hill wise",
        "", "HC Hill wise  cumulative",
        f"CO({unit})", "CO Hill wise",
        "", "CO Hill wise  cumulative",
        f"NOx({unit})", "NOx Hill wise",
        "", "NOx Hill wise cumulative",
        "SPEED", "HC Mode wise",
        "RPM", "CO Mode wise",
        "Stepper opening", "NOx Mode wise",
        "Throttle opening", "Throttle opening hill wise",
        "CLC (Lambda corrections)", "CLC Mode wise",
        "COILADV1 (primary ign)", "Primary Ign Timing",
        "COILADV2 (Secondary ign)", "WMTC START DATA",
        "AF_FUELOFFSET (Fuel learning)", "",
        "INJQUANT1 (Fuel injection quantity (mg))", "WMTC END DATA",
        "STATICFUELCOMP (% overall Fuel compensation)", "",
        "EWTFUELCOMP (% temp based fuel compensation)", "WMTC MIN MAX DATA",
        "EWTADVCOMP (% temp based ign compenstation)", "",
        "LAMBDAV1 (lambda sensor voltage)", "",
        "pu & Manifold air pressure", "ERROR History",
        "EVAPFLOW", "",
        "MILFAULT", ""

            ]

    else:
        fixed_layout_titles = ["", "",
                          "", "",
                          f"HC({unit})", "HC Hill wise",
                          "", "HC Hill wise  cumulative",
                          f"CO({unit})", "CO Hill wise",
                          "", "CO Hill wise  cumulative",
                          f"NOx({unit})", "NOx Hill wise",
                          "", "NOx Hill wise cumulative",
                          "SPEED", "HC Mode wise",
                          "cps_n_engine", "CO Mode wise",
                          "ecarb_pct_solenoid_PWM", "NOx Mode wise",
                          "tps_pct_throttle_position", "Throttle opening hill wise",
                          "ecarb_U_lm_sensor_signal", "Primary Ign Timing",
                          "ecarb_deg_primary_ign","",
                          "ecarb_pct_take_off_PWM", "WMTC START DATA",
                          "ecarb_b_orc_condition","",
                          "ecarb_sv_control_state","WMTC END DATA",
                          "afm_b_mil_active","",
                          "afm_b_vss_fault_active", "WMTC MIN MAX DATA",
                          "ecarb_b_idle_control_active","",
                          "cps_cnt_pip_reset_fault","",
                          "ecarb_T_engine_temp","ERROR History",
                          "tps_U_sensor","",
                          "ecarb_deg_secondary_ign","",
                          ]

    row_heights = [0.01, 0.01*len(etr_no_required), 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.05, 0.05,
                   0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05,
                   0.05,
                   0.05, 0.05,
                   0.05, 0.05, 0.05]#two for observation table

    variable_layout = []
    for i in inca_variables_additional:
        variable_layout.append([{"type": "scatter"}, {"type": "Bar"}])
        row_heights.append(0.05)

    #variable_layout = np.array(variable_layout).reshape(len(inca_variables_additional), 2)

    variable_layout_titles = []
    for i in inca_variables_additional:
        variable_layout_titles.append(i)
        variable_layout_titles.append("")


    observation_table_layout = [
        [{"type": "Table", "rowspan": 2}, {"type": "Table"}],
        [{"type": "Table"}, {"type": "Table"}]
    ]

    observation_table_layout_titles = ["", "", "", ""]

    plotly_fig = make_subplots(
        rows=26 + len(inca_variables_additional), cols=2,
        column_widths=[0.65, 0.35],
        specs=fixed_layout + variable_layout + observation_table_layout,
        vertical_spacing=0.015,
        horizontal_spacing=0.05,
        subplot_titles=fixed_layout_titles + variable_layout_titles + observation_table_layout_titles,
        row_heights=row_heights
    )

    ########################################################################################################################
    # COLLECTING MODAL AND INCA DATA
    modal_plotly_data = {}
    inca_plotly_data = {}
    colors = ["#ff6666", "#0099ff", "#00cc66", "#FFFE37", "#13F4EF", "#FF6133", "#2A3DFF", "#56FF68", "#FFCC56",
              "#FF6C00", "#ff6666", "#0099ff", "#00cc66", "#FFFE37", "#13F4EF", "#FF6133", "#2A3DFF", "#56FF68", "#FFCC56",
              "#FF6C00"
              ]
    c = 0
    for n in etr_no_required:
        modal_plotly_data[n] = []
        inca_plotly_data[n] = []

        speed_signal_with_legend = go.Scatter(y=modal_df_list[n]["Speed"],
                                  mode='lines',
                                  name="Speed",
                                  opacity=0.6,
                                  line=dict(color="#6b6b6b",
                                            shape="spline" if smooth == 1 else "linear",
                                            width=0.5,
                                            ),
                                  legendgroup="Speed",
                                  showlegend=True,
                                  hoverinfo="skip"
                                  )

        speed_signal_wo_legend = go.Scatter(y=modal_df_list[n]["Speed"],
                                              mode='lines',
                                              name="Speed",
                                              opacity=0.6,
                                              line=dict(color="#6b6b6b",
                                                        shape="spline" if smooth == 1 else "linear",
                                                        width=0.5,
                                                        ),
                                              legendgroup="Speed",
                                              showlegend=False,
                                              hoverinfo="skip"
                                              )

        for v in range(len(modal_variables)):
            modal_plotly_data[n].append(go.Scatter
                (
                y=modal_df_list[n][modal_variables[v]],
                mode='lines',
                name=str(n) if modal_variables[v] == "Speed" else str(n),
                line=dict(color=colors[c],
                          shape="spline" if smooth == 1 else "linear"),
                legendgroup=str(n),
                showlegend=True if modal_variables[v] == "Speed" else False,
                #text="comment1"
            )
            )


        for v in range(len(inca_variables + inca_variables_additional)):
            try:
                y = inca_df_list[n][inca_variables[v]][start_row[n]:end_row[n]] if v < len(inca_variables) else inca_df_list[n][inca_variables_additional[v - len(inca_variables)]][start_row[n]:end_row[n]]
            except:
                try:
                    y = inca_df_list[n][inca_variables[v]][start_row[n]:] if v < len(inca_variables) else inca_df_list[n][inca_variables_additional[v - len(inca_variables)]][start_row[n]:]
                except:
                    y = []

            inca_plotly_data[n].append(
                go.Scatter
                    (
                    y=y,
                    mode='lines',
                    name=inca_variables[v] + str(n) if v < len(inca_variables) else inca_variables_additional[v - len(inca_variables)] + str(n),
                    line=dict(color=colors[c],
                              shape="spline" if smooth == 1 else "linear"),
                    legendgroup=str(n),
                    showlegend=False
                )

            )
        c = c + 1

    #print(inca_plotly_data)

    ########################################################################################################################
    # PLOTTING MODAL AND INCA DATA
    for i in range(3):
        speed_counter = 0
        for n in etr_no_required:
            if speed_counter == 0:
                plotly_fig.add_trace(speed_signal_with_legend if i == 0 else speed_signal_wo_legend,
                                     row=3 + 2 * i,
                                     col=1,
                                     secondary_y=True
                                     )
            else:
                plotly_fig.add_trace(speed_signal_wo_legend if i == 0 else speed_signal_wo_legend,
                                     row=3 + 2 * i,
                                     col=1,
                                     secondary_y=True
                                     )
            if unit == "ppm":
                plotly_fig.add_trace(modal_plotly_data[n][4 + i],
                                     row=3 + 2*i,
                                     col=1,
                                     secondary_y=False
                                     )
            else:
                plotly_fig.add_trace(modal_plotly_data[n][1+i],
                                     row=3 + 2 * i,
                                     col=1,
                                     secondary_y=False
                                     )

            speed_counter += 1

    for n in etr_no_required:
        plotly_fig.add_trace(modal_plotly_data[n][0],
                             row=9,
                             col=1,
                             )

    for i in range(3):
        for n in etr_no_required:
            plotly_fig.add_trace(inca_plotly_data[n][i],
                                 row=10 + i,
                                 col=1
                                 )


    #print(inca_plotly_data)
    if vdpl == 0:
        for i in range(3, 5 if ecarb == 0 else 4):
            for n in etr_no_required:
                plotly_fig.add_trace(inca_plotly_data[n][i],
                                     row=13,
                                     col=1
                                     )

        for i in range(5, 13):
            for n in etr_no_required:
                plotly_fig.add_trace(inca_plotly_data[n][i],
                                     row=9 + i,
                                     col=1
                                     )
        try:
            for i in range(13, 15 if ecarb == 0 else 14):
                for n in etr_no_required:
                    plotly_fig.add_trace(inca_plotly_data[n][i],
                                        row=22,
                                        col=1
                                        )
            for i in range(15, 17):
                for n in etr_no_required:
                    plotly_fig.add_trace(inca_plotly_data[n][i],
                                        row=8+i,
                                        col=1
                                        )

            for i in range(19, 19 + len(inca_variables_additional)):
                for n in etr_no_required:
                    plotly_fig.add_trace(inca_plotly_data[n][i],
                                        row=6+i,
                                        col=1
                                        )
        except:
            pass
    else:
        for i in range(3, 5 ):
            for n in etr_no_required:
                plotly_fig.add_trace(inca_plotly_data[n][i],
                                     row=13,
                                     col=1
                                     )

        for i in range(5, 13):
            for n in etr_no_required:
                plotly_fig.add_trace(inca_plotly_data[n][i],
                                     row=9 + i,
                                     col=1
                                     )
        for i in range(13, 15 ):
            for n in etr_no_required:
                plotly_fig.add_trace(inca_plotly_data[n][i],
                                     row=22,
                                     col=1
                                     )
        for i in range(15, 17):
            for n in etr_no_required:
                plotly_fig.add_trace(inca_plotly_data[n][i],
                                     row=8 + i,
                                     col=1
                                     )

        for i in range(19, 19 + len(inca_variables_additional)):
            for n in etr_no_required:
                plotly_fig.add_trace(inca_plotly_data[n][i],
                                     row=6 + i,
                                     col=1
                                     )

    plotly_fig.update_xaxes(matches='x')
    plotly_fig.update_xaxes(showticklabels=True, row=5, col=1)
    # plotly_fig['layout']['yaxis2']['showgrid'] = False
    plotly_fig.update_layout(yaxis5=dict(showgrid=False,
                                           showticklabels=False,
                                         automargin=True)
                             )
    plotly_fig.update_layout(yaxis11=dict(showgrid=False,
                                         showticklabels=False,
                                          fixedrange=True
                                         )
                             )
    plotly_fig.update_layout(yaxis17=dict(showgrid=False,
                                         showticklabels=False,
                                          fixedrange=True
                                         )
                             )

    if bosch == 1:
        plotly_fig.update_yaxes(range=[0.75, 1.25], row=13, col=1)
        plotly_fig.update_yaxes(range=[-2, 2], row=15, col=1)
        plotly_fig.update_yaxes(range=[0.75, 1.25], row=16, col=1)
        plotly_fig.update_yaxes(range=[0.75, 3.5], row=17, col=1)
        plotly_fig.update_yaxes(range=[0.8, 1.2], row=18, col=1)
        plotly_fig.update_yaxes(range=[-5, 5], row=19, col=1)
        plotly_fig.update_yaxes(range=[0, 100], row=21, col=1)
        plotly_fig.update_yaxes(range=[0, 1000], row=22, col=1)

    elif vdpl == 1:
        plotly_fig.update_yaxes(range=[-15, 15], row=13, col=1)
        plotly_fig.update_yaxes(range=[0, 40], row=14, col=1)
        plotly_fig.update_yaxes(range=[0, 40], row=15, col=1)
        plotly_fig.update_yaxes(range=[0, 20], row=17, col=1)
        plotly_fig.update_yaxes(range=[0, 100], row=22, col=1)


    #plotly_fig.add_annotation(text="comment", align="right", showarrow=False, yshift=-10, clicktoshow="onoff", row=3, col=1)
    ########################################################################################################################
    # INITIALISING WITH EMPTY DATA STRUCTURE
    hill_wise_data = {}
    cumulative_percentage = {}
    for n in etr_no_required:
        hill_wise_data[n] = {}
        cumulative_percentage[n] = {}
        hill_wise_data[n]["HC_g/s"] = []
        hill_wise_data[n]["CO_g/s"] = []
        hill_wise_data[n]["NOx_g/s"] = []
        cumulative_percentage[n]["HC_g/s"] = []
        cumulative_percentage[n]["CO_g/s"] = []
        cumulative_percentage[n]["NOx_g/s"] = []

    ########################################################################################################################
    # HILL WISE MODAL PARAMETERS
    pollutants = ["HC_g/s", "CO_g/s", "NOx_g/s"]
    for p in pollutants:
        for n in range(len(etr_no_required)):
            wmtc_class = wmtc_class_list[n]
            for i in range(len(P1H[wmtc_class]["start"])):
                start = P1H[wmtc_class]["start"][i]
                end = P1H[wmtc_class]["end"][i]
                pollutant_cumulative = 0
                for j in range(start, end):
                    try:
                        pollutant_cumulative = pollutant_cumulative + modal_df_list[etr_no_required[n]][p][j]
                    except:
                        pass

                hill_wise_data[etr_no_required[n]][p].append(pollutant_cumulative)

            for i in range(len(P2H[wmtc_class]["start"])):
                start = P2H[wmtc_class]["start"][i]
                end = P2H[wmtc_class]["end"][i]
                pollutant_cumulative = 0
                for j in range(start, end):
                    try:
                        pollutant_cumulative = pollutant_cumulative + modal_df_list[etr_no_required[n]][p][j]
                    except:
                        pass

                hill_wise_data[etr_no_required[n]][p].append(pollutant_cumulative)

            if wmtc_class > 30:
                for i in range(len(P3H[wmtc_class]["start"])):
                    start = P3H[wmtc_class]["start"][i]
                    end = P3H[wmtc_class]["end"][i]
                    pollutant_cumulative = 0
                    for j in range(start, end):
                        try:
                            pollutant_cumulative = pollutant_cumulative + modal_df_list[etr_no_required[n]][p][j]
                        except:
                            pass

                    hill_wise_data[etr_no_required[n]][p].append(pollutant_cumulative)

            #calculating cumulative percentages
            total = sum(hill_wise_data[etr_no_required[n]][p])
            for i in range(len(hill_wise_data[etr_no_required[n]][p])):
                x = 0
                for j in range(i + 1):
                    x = x + hill_wise_data[etr_no_required[n]][p][j]
                #x_per = (x/total)*100
                #x_per = x_per.__round__(1)
                #print(x_per)
                cumulative_percentage[etr_no_required[n]][p].append(x)


    for p in range(len(pollutants)):
        count = 0
        for n in etr_no_required:
            plotly_fig.add_trace(go.Bar(name=pollutants[p][:-4] + " gm " + str(n),
                                        #text=pollutants[p],
                                        x=["H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10",
                                           "H11", "H12", "H13", "H14", "H15", "H16", "H17", "H18", "H19", "H20",
                                           "H21", "H22", "H23", "H24", "H25", "H26", "H27", "H28", "H29",
                                           "H30"],
                                        y=hill_wise_data[n][pollutants[p]],
                                        marker=dict(color=colors[count]),
                                        showlegend=True if p == "HC_g/s" else False,
                                        legendgroup=str(n)),
                                 row=2*p + 3,
                                 col=2,

                                 )
            plotly_fig.add_trace(go.Scatter(name=pollutants[p][:-4] + " gm " + str(n),
                                        #text=pollutants[p],
                                        x=["H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10",
                                           "H11", "H12", "H13", "H14", "H15", "H16", "H17", "H18", "H19", "H20",
                                           "H21", "H22", "H23", "H24", "H25", "H26", "H27", "H28", "H29",
                                           "H30"],
                                        y=cumulative_percentage[n][pollutants[p]],
                                        marker=dict(color=colors[count]),
                                        showlegend=True if p == "HC_g/s" else False,
                                        legendgroup=str(n)),
                                 row=2*p + 3 + 1,
                                 col=2,

                                 )
            count = count + 1
        plotly_fig.update_layout(barmode='group')

    ########################################################################################################################
    # HILL WISE INCA PARAMETERS
    # EMS BASED HILL WISE PARAMETERS
    if bosch == 1:
        hill_wise_inca_parameteres = ["wdkba_w"]
    elif ecarb == 1:
        hill_wise_inca_parameteres = ["tps_pct_throttle_position"]
    elif vdpl == 1:
        hill_wise_inca_parameteres = ["TPS"]
    elif mikuni == 1:
        hill_wise_inca_parameteres = ["g_Thp_Val"]
    else:
        hill_wise_inca_parameteres = [" "]

    hill_wise_inca_data = {}
    for n in etr_no_required:
        hill_wise_inca_data[n] = {}
        if bosch == 1:
            hill_wise_inca_data[n]["wdkba_w"] = []
        elif ecarb == 1:
            hill_wise_inca_data[n]["tps_pct_throttle_position"] = []
        elif vdpl == 1:
            hill_wise_inca_data[n]["TPS"] = []
        elif mikuni == 1:
            hill_wise_inca_data[n]["g_Thp_Val"] = []
        else:
            hill_wise_inca_data[n][" "] = []

    for p in hill_wise_inca_parameteres:
        for n in range(len(etr_no_required)):
            wmtc_class = wmtc_class_list[n]
            skip = start_row[etr_no_required[n]]
            for i in range(len(P1H[wmtc_class]["start"])):
                start = P1H[wmtc_class]["start"][i]
                end = P1H[wmtc_class]["end"][i]
                inca_parameter = []
                for j in range(start + skip, end + skip):
                    try:
                        inca_parameter.append(inca_df_list[etr_no_required[n]][p][j])
                    except:
                        pass
                try:
                    hill_wise_inca_data[etr_no_required[n]][p].append(statistics.mean(inca_parameter))
                except:
                    hill_wise_inca_data[etr_no_required[n]][p].append(0)

            for i in range(len(P2H[wmtc_class]["start"])):
                start = P2H[wmtc_class]["start"][i]
                end = P2H[wmtc_class]["end"][i]
                inca_parameter = []
                for j in range(start + skip, end + skip):
                    try:
                        inca_parameter.append(inca_df_list[etr_no_required[n]][p][j])
                    except:
                        pass
                try:
                    hill_wise_inca_data[etr_no_required[n]][p].append(statistics.mean(inca_parameter))
                except:
                    hill_wise_inca_data[etr_no_required[n]][p].append(0)

            if wmtc_class > 30:
                for i in range(len(P3H[wmtc_class]["start"])):
                    start = P3H[wmtc_class]["start"][i]
                    end = P3H[wmtc_class]["end"][i]
                    inca_parameter = []
                    for j in range(start + skip, end + skip):
                        try:
                            inca_parameter.append(inca_df_list[etr_no_required[n]][p][j.__round__(0)])
                        except:
                            pass
                    try:
                        hill_wise_inca_data[etr_no_required[n]][p].append(statistics.mean(inca_parameter))
                    except:
                        hill_wise_inca_data[etr_no_required[n]][p].append(0)

    # PLOTTING HILL WISE INCA DATA
    counter1 = 0
    for p in hill_wise_inca_parameteres:
        count = 0
        for n in etr_no_required:
            plotly_fig.add_trace(go.Bar(name=p + " avg " + str(n),
                                        #text=hill_wise_inca_parameteres[counter1],
                                        x=["H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10",
                                           "H11", "H12", "H13", "H14", "H15", "H16", "H17", "H18", "H19", "H20",
                                           "H21", "H22", "H23", "H24", "H25", "H26", "H27", "H28", "H29",
                                           "H30"],
                                        y=hill_wise_inca_data[n][p],
                                        marker=dict(color=colors[count]),
                                        legendgroup=str(n),
                                        showlegend=False),
                                 row=counter1 + 12,
                                 col=2,

                                 )
            count = count + 1
        counter1 = counter1 + 1

        plotly_fig.update_layout(barmode='group')

    ######################################################################################################################
    # MODE WISE POLLUTANT DATA COLLECTION
    mode_wise_data = {}
    for n in etr_no_required:
        mode_wise_data[n] = {}
        for p in pollutants:
            mode_wise_data[n][p] = {}
            for m in modes:
                mode_wise_data[n][p][m] = []

    for p in pollutants:
        for m in modes:
            for n in etr_no_required:
                part = 0
                pollutant_cumulative = 0
                for pa in parts[n]:
                    for i in range(len(phases[pa][m]["start"])):
                        start = phases[pa][m]["start"][i]
                        end = phases[pa][m]["end"][i]
                        for j in range(start, end):
                            try:
                                pollutant_cumulative = pollutant_cumulative + modal_df_list[n][p][part * 600 + j]
                            except:
                                pass
                    part = part + 1
                try:
                    #mode_wise_data[n][p][m].append(100*pollutant_cumulative/sum(modal_df_list[n][p]))
                    mode_wise_data[n][p][m].append(pollutant_cumulative)
                except:
                    mode_wise_data[n][p][m].append(0)

    ####################################################################################################################
    # MODE WISE POLLUTANT PLOTTING
    r = 9
    for p in pollutants:
        count = 0
        for n in etr_no_required:
            y = []
            for m in modes:
                y.append(mode_wise_data[n][p][m][0])

            plotly_fig.add_trace(
                go.Bar(
                    name=p[:-4] + " " + str(n),
                    x=modes,
                    y=y,
                    marker=dict(color=colors[count]),
                    legendgroup=str(n),
                    showlegend=False
                ),
                row=r,
                col=2
            )
            count = count + 1

        plotly_fig.update_layout(barmode='group')
        plotly_fig.update_annotations(x=modes[0], text="IDLE", row=r, col=2)

        r = r + 1

    ########################################################################################################################
    # MODE WISE INCA DATA COLLECTION
    mode_wise_inca_data = {}
    if bosch == 1:
        parameters = ["fr_w", "zwout"]
    elif ecarb == 1:
        parameters = ["ecarb_deg_primary_ign"]
    elif vdpl == 1 :
        parameters = ["CLC", "COILADV1"]
    elif mikuni == 1:
        parameters = ["g_O2fb_Cps","g_Ign_Tmg"]
    else:
        parameters = [" "]
    for n in etr_no_required:
        mode_wise_inca_data[n] = {}
        for p in parameters:
            mode_wise_inca_data[n][p] = {}
            for m in modes:
                mode_wise_inca_data[n][p][m] = []

    for p in parameters:
        for m in modes:
            for n in etr_no_required:
                part = 0
                for pa in parts[n]:
                    inca_parameter = []
                    for i in range(len(phases[pa][m]["start"])):
                        start = phases[pa][m]["start"][i]
                        end = phases[pa][m]["end"][i]
                        for j in range(start, end):
                            try:
                                inca_parameter.append(inca_df_list[n][p][600 * part + j])
                            except:
                                pass
                    part = part + 1
                try:
                    mode_wise_inca_data[n][p][m].append(statistics.mean(inca_parameter))
                except:
                    mode_wise_inca_data[n][p][m].append(0)

    # MODE WISE INCA DATA PLOTTING
    r = 13
    for p in parameters:
        count = 0
        for n in etr_no_required:
            y = []
            for m in modes:
                y.append(mode_wise_inca_data[n][p][m][0])

            plotly_fig.add_trace(
                go.Bar(
                    name=p + " " + str(n),
                    x=modes,
                    y=y,
                    marker=dict(color=colors[count]),
                    legendgroup=str(n),
                    showlegend=False),
                row=r,
                col=2
            )
            count = count + 1
        plotly_fig.update_layout(barmode='group')
        if bosch == 1:
            plotly_fig.update_yaxes(range=[0.85, 1.05], row=13, col=2)
        elif vdpl == 1:
            plotly_fig.update_yaxes(range=[-5, 5], row=13, col=2)

        r = r + 1


    ########################################################################################################################
    # GETTING EMISSION RESULT FROM CSV

    csv_df = pd.read_csv(single_line_csv_path,  low_memory=False, encoding='unicode_escape')
    csv_df.fillna('NA', inplace=True)
    # COLLECTING DATA FOR OVERVIEW TABLE

    parameters = ["MODEL", "CO%", "HC%", "NOX%", "NMHC%", "CB",
                   "CO", "COP1", "COP2", "COP3",
                  "HC","HCP1", "HCP2", "HCP3",
                  "NOX","NOXP1", "NOXP2", "NOXP3",
                   "NMHC","NMHCP1", "NMHCP2", "NMHCP3"
                  ]
    location = [3, 11, 12, 13, 14, 16]#these are locations of Model, co, hc, nox, nmhc, cb


    table_data = {}
    phase_wise_pollutants_data = {}
    for n in etr_no_required:
        phase_wise_pollutants_data[n] = {}
        for i in range(1, 5):
            phase_wise_pollutants_data[n][parameters[i]] = []

    table_data["ETR NO"] = etr_no_required
    for p in parameters:
        table_data[p] = []
    for n in etr_no_required:
        try:
            etr_df = csv_df[csv_df.SN == int(n)].iloc[-1]
            for i in range(len(parameters)):
                try:
                    table_data[parameters[i]].append(etr_df[parameters[i]])
                except:
                    table_data[parameters[i]].append("NA")
        except:
            for i in range(len(parameters)):
                table_data[parameters[i]].append("NA")


    df = pd.DataFrame(table_data)

    fill_color_list = []
    font_color_list = []
    for i in range(df.shape[1]):
        if i == 0:
            color_list = []
            font_color = []
            for n in range(len(etr_no_required)):
                color_list.append(colors[n])
                font_color.append("#000000")

            fill_color_list.append(color_list)
            font_color_list.append(font_color)

        elif i == 1:
            color_list = []
            font_color = []

            for n in range(len(etr_no_required)):
                color_list.append(colors[n])
                font_color.append("#000000")

            fill_color_list.append(color_list)
            font_color_list.append("#000000")

        elif 2 <= i <= 5:
            color_list = []
            font_color = []

            for n in range(len(etr_no_required)):
                try:
                    if float(df.iloc[n][i]) <= 70:
                        color_list.append("#00b050")
                        font_color.append("#000000")
                    elif 70 < float(df.iloc[n][i]) < 85:
                        color_list.append("#f79646")
                        font_color.append("#000000")
                    elif 85 <= float(df.iloc[n][i]) < 100:
                        color_list.append("#FF0000")
                        font_color.append("#000000")
                    elif 100 <= float(df.iloc[n][i]):
                        color_list.append("#FF0000")
                        font_color.append("#FFFFFF")
                except:
                    color_list.append("#f29583")
                    font_color.append("#000000")

            fill_color_list.append(color_list)
            font_color_list.append(font_color)

        else:
            color_list = []
            font_color = []

            for n in etr_no_required:
                color_list.append("#dbeb9b")
                font_color.append("#000000")

            fill_color_list.append(color_list)
            font_color_list.append(font_color)

    plotly_fig.add_trace(go.Table(
        header=dict(values=list(df.columns),
                    line_color='darkslategray',
                    fill_color='black',
                    align =['center', 'center'],
                    font=dict(color='white', size=12)
                    ),
        cells=dict(values=df.transpose().values.tolist(),
                   fill_color=fill_color_list,
                   align=['center'],
                   font=dict(color=font_color_list, size=11),
                   height=25
                   ),
    ),
        row=1,
        col=1
    )


    ########################################################################################################################
    # INCA DATA TABLE
    if bosch == 1:
        start_parameters = ["tans", "tmot", "rka_w", "fra_w", "dmvad_w", "ofmsdkq_w"]
    elif ecarb == 1:
        start_parameters = ["ecarb_T_engine_temp"]
    elif vdpl == 1:
        start_parameters = ["MAT", "EWT", "AF_FUELOFFSET", "SLOWIACVI", "MILFAULT", "VBATT"]
    elif mikuni ==1:
        start_parameters = ["g_At_Val", "g_Wt_Val", "g_FuelWt_Cps"]
    else:
        start_parameters = [" "]

    inca_table_start_data = {}
    inca_table_start_data["ETR NO"] = etr_no_required
    for p in start_parameters:
        inca_table_start_data[p] = []
    if bosch == 1:
        end_parameters = ["tans", "tmot", "rka_w", "fra_w", "dmvad_w", "ofmsdkq_w"]
    elif ecarb == 1:
        end_parameters = ["ecarb_T_engine_temp"]
    elif vdpl == 1:
        end_parameters = ["MAT", "EWT", "AF_FUELOFFSET", "SLOWIACVI", "MILFAULT", "VBATT"]
    elif mikuni == 1:
        end_parameters = ["g_At_Val", "g_Wt_Val", "g_FuelWt_Cps"]
    else:
        end_parameters = [" "]

    inca_table_end_data = {}
    inca_table_end_data["ETR NO"] = etr_no_required
    for p in end_parameters:
        inca_table_end_data[p] = []

    inca_table_min_max_data  = {}
    inca_table_min_max_data["ETR NO"] = etr_no_required
    if bosch == 1:
        min_max_parameters = ["fr_w", "nmot_w", "pu", "wdkba_w"]
    elif ecarb == 1:
        min_max_parameters = ["ecarb_T_engine_temp", "tps_pct_throttle_position"]
    elif vdpl == 1:
        min_max_parameters = ["CLC", "RPM", "BARO", "TPS"]
    elif mikuni == 1:
        min_max_parameters = ["g_O2fb_Cps", "g_Crnk_Rev", "g_Iprs_PRat", "g_Thp_Val"]
    else:
        min_max_parameters = [" "]
    for p in min_max_parameters:
        inca_table_min_max_data["min " + p] = []
        inca_table_min_max_data["max " + p] = []

    def get_start_value(start_parameter, n):
        try:
            inca_table_start_data[start_parameter].append(inca_df_list[n][start_parameter][start_row[n]].__round__(2))
        except:
            inca_table_start_data[start_parameter].append("NA")


    def get_end_value(end_parameter, n):
        try:
            inca_table_end_data[end_parameter].append(inca_df_list[n][end_parameter][end_row[n]].__round__(2))
        except:
            try:
                inca_table_end_data[end_parameter].append(inca_df_list[n][end_parameter][end_row[n-5]].__round__(2))
            except:
                try:
                    inca_table_end_data[end_parameter].append(inca_df_list[n][end_parameter].iloc[-1].__round__(2))
                except:
                    inca_table_end_data[end_parameter].append("NA")

    def get_min_max_value(inca_parameter, n):
        try:
            inca_table_min_max_data["min " + inca_parameter].append(min(inca_df_list[n][inca_parameter]).__round__(2))
            inca_table_min_max_data["max " + inca_parameter].append(max(inca_df_list[n][inca_parameter]).__round__(2))
        except:
            inca_table_min_max_data["min " + inca_parameter].append("NA")
            inca_table_min_max_data["max " + inca_parameter].append("NA")

    for n in etr_no_required:
        for p in start_parameters:
            get_start_value(p, n)
        for p in end_parameters:
            get_end_value(p, n)
        for p in min_max_parameters:
            get_min_max_value(p, n)

    def plotting_inca_table(inca_table_data, r):
        print(inca_table_data)
        inca_table_df = pd.DataFrame(inca_table_data)
        inca_table_df = inca_table_df.transpose()
        inca_table_df.columns = inca_table_df.iloc[0]
        inca_table_df = inca_table_df[1:]
        inca_table_df = inca_table_df.reset_index()
        inca_table_df = inca_table_df.rename(columns={'index': 'VARIABLE'})
        print("completely OK")
        fill_color_list = []
        font_color_list = []
        for i in range(inca_table_df.shape[1]):
            if i == 0:
                color_list = []
                font_color = []
                for j in range(inca_table_df.shape[0]):
                    color_list.append("#ffcc26")
                    font_color.append("#000000")

                fill_color_list.append(color_list)
                font_color_list.append(font_color)

            else:
                color_list = []
                font_color = []
                for j in range(inca_table_df.shape[0]):
                    color_list.append("#03fcf8")
                    font_color.append("#000000")

                fill_color_list.append(color_list)
                font_color_list.append(font_color)

        plotly_fig.add_trace(go.Table(
            columnwidth=[2,1],
            header=dict(values=list(inca_table_df.columns),
                        line_color='darkslategray',
                        fill_color='black',
                        ),
            cells=dict(values=inca_table_df.transpose().values.tolist(),
                       fill_color=fill_color_list,
                       align=['center'],
                       font=dict(color=font_color_list),
                       height=25
                       ),
        ),
            row=r,
            col=2
        )

    plotting_inca_table(inca_table_start_data, 15)
    plotting_inca_table(inca_table_end_data, 17)
    plotting_inca_table(inca_table_min_max_data, 19)



    ########################################################################################################################
    # ERROR TABLE
    #creating empty dictionary for storing error data
    num_dfc = {}
    stchk = {}
    #seperate dictionary for error name and status for each etr number
    for n in etr_no_required:
        num_dfc[n] = {}
        stchk[n] = {}
        #for each error there will be list that will contain its status upto 5 errors can be stored
        for i in range(5):
            num_dfc[n][i] = []
            stchk[n][i] = []
        try:
            df = error_df_list[n]
            #this gives a seperate list for each column where there is change in value so it's a list of list
            error_history = df.ne(df.shift()).apply(lambda x: x.index[x].tolist())
            for j in range(5):
                #error name can at max have two values either from unused to some defect entry or it will be there from previous cycle
                num_dfc[n][j].append(df[df.columns[j]][error_history[j][-1]])
                for k in range(len(error_history[j + 5])):
                    stchk[n][j].append(df[df.columns[j + 5]][error_history[j + 5][k]])

        except:
            pass

    error_table_data = {}
    error_table_data["ETR NO "] = []
    error_table_data["ERROR NAME"] = []
    error_table_data["HISTORY"] = []

    for n in etr_no_required:
        for i in range(5):
            try:
                if not str(num_dfc[n][i][-1]) == "b'DFC_Unused'":
                    history = ""
                    error_table_data["ETR NO "].append(n)
                    error_table_data["ERROR NAME"].append(str(num_dfc[n][i][-1]))
                    for j in range(len(stchk[n][i])):
                        history = history + "\n " + str(stchk[n][i][j])
                    error_table_data["HISTORY"].append(history)
            except:
                pass

    error_table_df = pd.DataFrame(error_table_data)

    plotly_fig.add_trace(go.Table(
        columnwidth=[1, 3, 2],
        header=dict(values=list(error_table_df.columns),
                    line_color='darkslategray',
                    fill_color='black',
                    font=dict(color='white', size=12)
                    ),
        cells=dict(values=error_table_df.transpose().values.tolist(),
                   fill_color="#03fcf8",
                   # fill_color="black",
                   align=['center'],
                   font=dict(color='black')
                   ),
    ),
        row=22,
        col=2
    )
    ########################################################################################################################
    # REMARKS / Observations
    observation_data = {}
    observation_data["SN"] = [1,2,3,4,5]
    observation_data["Observations "] = ["","","","",""]

    for i in range(5):
        try:
            observation_data["Observations "][i] = remark_dict[remark_entries[i]].get("1.0",tk.END)
        except:
            observation_data["Observations "][i] = remarks[i]

    obs_df = pd.DataFrame(observation_data)
    plotly_fig.add_trace(go.Table(
        columnwidth =[1,9],
        header=dict(values=list(obs_df.columns),
                    line_color='darkslategray',
                    fill_color='black',
                    font=dict(color='white', size=20)
                    ),
        cells=dict(values=obs_df.transpose().values.tolist(),
                   fill_color=["#03fcf8","white"],
                   align=['center', 'left'],
                   font=dict(color='black', size = 20),
                   height = 50
                   ),
    ),
        row=25 + len(inca_variables_additional),
        col=1
    )

    ########################################################################################################################
    # UPDATING FIGURE LAYOUT
    # test_report_number = pd.read_csv(run_details_csv).SN.values[-1] + 1
    plotly_fig.update_layout(
        title_text="ETR REPORT NO " + str(1) + "  " + str(etr_no_required) if call == html_report else "ETR " + str(etr_no_required),
        autosize=False,
        #template='plotly_dark',
        template='simple_white' if ltheme == 1 else "plotly_dark",
        width=1600,
        height=5000,
        #hovermode="x"
        hovermode="x unified",
        hoverlabel=dict(bgcolor='rgba(255,255,255,0.6)',
                        bordercolor='rgba(255,255,255,0)',
                        # font_family="Arial Black",
                        font=dict(color='black')
                        )
    )

    plotly_fig.update_xaxes(color="#a8a5a5")
    plotly_fig.update_yaxes(color="#a8a5a5")
    return plotly_fig

if __name__ == "__main__":
    if etr_entry_mode == 1:
        all_mdf_files = os.listdir(mdf_file_path)
        all_mdf_files = [x[:-4][3:] for x in all_mdf_files if "ETR" in x]
        all_mdf_files = [int(x) for x in all_mdf_files if x.isdigit()]
        all_mdf_files = [int(x) for x in all_mdf_files if x > 11500]
        all_html_reports = os.listdir(etr_report_location)
        all_html_reports = [x[:-5][3:] for x in all_html_reports if "ETR" in x]
        all_html_reports = [int(x) for x in all_html_reports if x.isdigit()]
        all_html_reports = [int(x) for x in all_html_reports if x > 11500]
        html_reports_to_made = sorted(set(all_mdf_files) - set(all_html_reports))
        # html_reports_to_made = ["11560"]
        wmtc_class_list = []
        remarks = ["", "", "", "", "", "", ""]
        error_generating_html = []
        for i in html_reports_to_made:
            try:
                html_report([str(i)],
                                        inca_variables_additional=[],
                                        wmtc_class_list=[],
                                        remark_dict={},
                                        remark_entries=[],
                                        ltheme=0,
                                        smooth=0,
                                        ecarb=0,
                                        vdpl = 1,
                                        tid=0
                                        )
            except:
                error_generating_html.append(i)

    else:
        etr_no_required = ["12521", "12523"]
        html_report(etr_no_required,
                    inca_variables_additional=[],
                    wmtc_class_list=[],
                    remark_dict={},
                    remark_entries=[],
                    ltheme=0,
                    smooth=0,
                    ecarb=0,
                    vdpl=1,
                    tid=0,
                    call="html_report",
                    unit="g/s"
                    )
