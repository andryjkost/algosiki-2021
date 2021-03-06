from path import *
# import solution
# import general_vns
from vns_1 import *
from solution import *


def print_solution_if_file(file_name, solution, machines_number, details_number):
    with open(file_name + '.sol', 'w') as out_file:
        cluster_id = 0
        machine_result_dict = dict()
        details_result_dict = dict()
        for cluster in solution["clusters_dict"]:
            cluster_id += 1
            for machine in cluster["machines"]:
                machine_result_dict[machine] = cluster_id
            for detail in cluster["details"]:
                details_result_dict[detail] = cluster_id
        for i in range(1, machines_number + 1):
            out_file.write(str(machine_result_dict[i]) + ' ')
        out_file.write('\n')
        for i in range(1, details_number + 1):
            out_file.write(str(details_result_dict[i]) + ' ')
        out_file.write('\n')
        out_file.write(str(solution["objectiveFunctionValue"]))


def print_solution(solution, machines_number, details_number):
        cluster_id = 0
        machine_result_dict = dict()
        details_result_dict = dict()
        for cluster in solution["clusters_dict"]:
            cluster_id += 1
            for machine in cluster["machines"]:
                machine_result_dict[machine] = cluster_id
            for detail in cluster["details"]:
                details_result_dict[detail] = cluster_id
        for i in range(1, machines_number + 1):
            print(str(machine_result_dict[i]),end=' ')
        print('/n')
        for i in range(1, details_number + 1):
            print(str(details_result_dict[i]),end=' ')
        print('/n')
        print(str(solution["objectiveFunctionValue"]))
        print('/n')
        print('/n')


if __name__ == '__main__':
    file_name = 'mosier20'
    info = dict()
    machines_number = 0
    details_number = 0
    matrix = list()

    info = get_info(file_name + '.txt', info)
    solution = vns(info["data_matrix"], info["mashines_number"], info["details_number"])
    print_solution_if_file(file_name, solution, info["mashines_number"], info["details_number"])
"""  info["mashines_number"] = int(re.findall('[0-9]+', data[0])[0])
    info["details_number"] = int(re.findall('[0-9]+', data[0])[1])
    info["data_dict"] = dict()   info["data_matrix"]"""

# solver = general_vns.GeneralVNS(_issue.data_matrix, _issue.machines_number, _issue.details_number)
# solution = solver.solution
# print_solution_if_file(file_name, solution, machines_number, details_number)
