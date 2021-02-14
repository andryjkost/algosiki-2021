import re
import numpy as np


def get_info(file_name,  info):
    file = open('./cfp/' + file_name)
    data = file.read().split('\n')
    info["mashines_number"] = int(re.findall('[0-9]+', data[0])[0])
    info["details_number"] = int(re.findall('[0-9]+', data[0])[1])
    info["data_dict"] = dict()
    for i in range(1, len(data)):
        machine_details_data = re.findall('[0-9]+', data[i])
        machine_id = int(machine_details_data[0])
        details_list = [int(i) for i in machine_details_data[1:]]
        info["data_dict"][machine_id] = details_list

    info["data_matrix"] = np.zeros([info["mashines_number"],  info["details_number"]], dtype=np.int)
    for key, values in info["data_dict"].items():
        for value in values:
            info["data_matrix"][key - 1, value - 1] = 1

    return info









