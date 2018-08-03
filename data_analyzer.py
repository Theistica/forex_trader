import os
import glob
import pandas as pd
import re

def format_data(folder_name):
    file_names = list_files(folder_name)
    header_names = ["date", "open", "high", "low", "close", "volume"]
    first_file = True
    for one_file in file_names:
        one_file_data = pd.read_csv(one_file, delimiter=";", names=header_names)
        one_file_data["date"] = one_file_data["date"].map(lambda x: re.sub("[^0-9]", "", x))
        if first_file:
            all_file_data = one_file_data
            first_file = False
        else:
            all_file_data = all_file_data.append(one_file_data, ignore_index=True)
        print ("worked for " + one_file)

    all_file_data.to_csv("data.csv")

def list_files(folder_name):
    file_names = []
    for subfolder_name in os.listdir(folder_name):
        for one_file in os.listdir(folder_name + "/" + subfolder_name):
            if one_file.endswith(".csv"):
                file_names.append(folder_name + "/" + subfolder_name + "/" + one_file)
    return file_names


if __name__ == '__main__':
    format_data("data")
