import os
import datetime
from pathlib import Path

def write_logs(POLICY_NUMBER,NEW_REGNUMBER,OLD_REGNUMBER,NEW_CHASSIS_NUMBER,OLD_CHASSIS_NUMBER,OlD_NAME,NEW_NAME,UPDATE):

    # Checking what type of update the user wants to make
    if UPDATE == "Reg_Update":
        Reg_Update = True
    else:
        Reg_Update = False
    if UPDATE ==  "Reg_and_chassis_Update":
        Reg_and_chassis_Update = True
    else:
        Reg_and_chassis_Update = False
    if UPDATE == "chassis_Update":
        chassis_Update = True
    else:
        chassis_Update = False
    if UPDATE == 'name_update':
        name_update = True
    else:
        name_update = False

    # Creating the LOGS Folder if it does not exist
    Log_folder_name = "LOGS"
    if Path(Log_folder_name).is_dir():
        print("")
    else:
        os.makedirs(Log_folder_name)

    # Geting the date and time
    current_datetime = datetime.datetime.now()
    # Formatting the Date and Time
    formatted_datetime = current_datetime.strftime("%Y-%m-%d")
    Date_and_Time = str(formatted_datetime)


    # Creating the log and folder file depending on which update was made
    if Reg_Update:
        POLICY_DETAILS = [f"POLICY NUMBER: {POLICY_NUMBER}", f"New Reg Number: {NEW_REGNUMBER}",
                          f"Old Reg NUMBER: {OLD_REGNUMBER}"]

        # Creating the RegCorrection log folder if it does not exist
        folder_name = "RegCorrection_logs"
        folder_path = "./LOGS/" + folder_name

        if Path(folder_path).is_dir():
            print("")
        else:
            os.makedirs(folder_path)
        logs_path = "./LOGS/RegCorrection_logs"
        log_file = formatted_datetime

        log_file_path = logs_path + "/" + log_file

    if Reg_and_chassis_Update:
        POLICY_DETAILS = [f"POLICY NUMBER: {POLICY_NUMBER}", f"New Reg Number: {NEW_REGNUMBER}",
                          f"Old Reg NUMBER: {OLD_REGNUMBER}", f"New Chassis Number: {NEW_CHASSIS_NUMBER}",
                          f"Old Chassis NUMBER: {OLD_CHASSIS_NUMBER}"]

        # Creating the RegCorrection log folder if it does not exist
        folder_name = "Reg and chassis Correction_logs"
        folder_path = "./LOGS/" + folder_name

        if Path(folder_path).is_dir():
            print("")
        else:
            os.makedirs(folder_path)
        logs_path = "./LOGS/Reg and chassis Correction_logs"
        log_file = formatted_datetime

        log_file_path = logs_path + "/" + log_file

    if chassis_Update:
        POLICY_DETAILS = [f"POLICY NUMBER: {POLICY_NUMBER}", f"New Chassis Number: {NEW_CHASSIS_NUMBER}",
                          f"Old Chassis NUMBER: {OLD_CHASSIS_NUMBER}"]
        # Creating the RegCorrection log folder if it does not exist
        folder_name = "Chassis_logs"
        folder_path = "./LOGS/" + folder_name

        if Path(folder_path).is_dir():
            print("")
        else:
            os.makedirs(folder_path)
        logs_path = "./LOGS/Chassis_logs"
        log_file = formatted_datetime

        log_file_path = logs_path + "/" + log_file

    if name_update:
        POLICY_DETAILS = [f"POLICY NUMBER: {POLICY_NUMBER}", f"New Name: {NEW_NAME}",
                          f"Old Name: {OlD_NAME}"]
        # Creating the RegCorrection log folder if it does not exist
        folder_name = "Name Correction_logs"
        folder_path = "./LOGS/" + folder_name

        if Path(folder_path).is_dir():
            print("")
        else:
            os.makedirs(folder_path)
        logs_path = "./LOGS/Name Correction_logs"
        log_file = formatted_datetime

        log_file_path = logs_path + "/" + log_file



    # Checking if the log file exist before writing or appending the file
    if Path(log_file_path).is_file():
        with open(log_file_path, "a") as logs:
            logs.write(f"Policy Details{POLICY_DETAILS}\n")
            logs.write(f"Date Modified {current_datetime}\n\n")
    else:
        with open(log_file_path, "w") as logs:
            logs.write(f"Policy Details{POLICY_DETAILS}\n")
            logs.write(f"Date Modified {current_datetime}\n\n")


