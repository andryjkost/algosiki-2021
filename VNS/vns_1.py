import random
from copy import deepcopy

from solution import Solution

from main_1 import print_solution

def getInitialSolution(data_matrix, machines_number, details_number):
    rand_machines = random.sample(range(1, machines_number), 10)
    rand_details = random.sample(range(1, details_number), 10)
    cluster_1 = {"machines": set(rand_machines), "details": set(rand_details), "data_matrix": data_matrix}

    other_machines = set(list(range(1, machines_number + 1))) - set(rand_machines)
    other_details = set(list(range(1, details_number + 1))) - set(rand_details)
    cluster_2 = {"machines": set(other_machines), "details": set(other_details), "data_matrix": data_matrix}
    init_solution = dict()
    init_solution["clusters_dict"], init_solution["objectiveFunctionValue"], init_solution[
        "numberOfClusters"] = Solution([cluster_1, cluster_2], data_matrix)
    return init_solution


def vns(data_matrix, machines_number, details_number):
    initial_solution = getInitialSolution(data_matrix, machines_number, details_number)
    curr_solution = local_serch(initial_solution,data_matrix)
    best_cost = 0.4801
    firs_cost= curr_solution["objectiveFunctionValue"]
    while best_cost > curr_solution["objectiveFunctionValue"]:
        peremennai_cost = curr_solution["objectiveFunctionValue"]
        if len(curr_solution["clusters_dict"]) == 1:
            curr_solution = divide(curr_solution
                                  , data_matrix, 0)
        else:
            list_solution = []
            merge_or_divide = random.randint(0, 1)
            ch = True
            while ch == True:
                ch = False
                for i in range(len(curr_solution["clusters_dict"])):
                    per_solution = divide(curr_solution, data_matrix, i)
                    list_solution.append(per_solution)
                perfect_sol= max(list_solution, key=lambda x: x["objectiveFunctionValue"])
                if perfect_sol["objectiveFunctionValue"] > curr_solution["objectiveFunctionValue"]:
                    curr_solution = perfect_sol
                    ch = True
                    print_solution(curr_solution, machines_number, details_number)
            ch = True
            while ch == True:
                ch = False
                for i in range(len(curr_solution["clusters_dict"])):
                    for j in range(i+1,len(curr_solution["clusters_dict"])):
                        flex_sol = merge(curr_solution, data_matrix, i,j)
                        list_solution.append(flex_sol)
                perfect_sol = max(list_solution, key=lambda x: x["objectiveFunctionValue"])
                if perfect_sol["objectiveFunctionValue"] > curr_solution["objectiveFunctionValue"]:
                    curr_solution = perfect_sol
                    ch = True
                    print_solution(curr_solution, machines_number, details_number)

    return curr_solution


    # while best_cost > curr_solution["objectiveFunctionValue"]:
    #     shaking_result = shaking(curr_solution, data_matrix)
    #     new_solution = local_serch(shaking_result, data_matrix)
    #     if new_solution["objectiveFunctionValue"] > curr_solution["objectiveFunctionValue"]:
    #         curr_solution = new_solution
    #         print_solution(curr_solution, machines_number, details_number)
    #
    #
    # return shaking_result


def shaking(solution, data_matrix):
    if len(solution["clusters_dict"]) == 1:
        new_solution = divide(solution, data_matrix,0)
    else:
        list_solution = []
        merge_or_divide = random.randint(0, 1)
        ch = True
        while ch == True:
            ch= False
            for  i in range(len(solution["dict_clusters"])):
                curr_solution = divide(solution, data_matrix,i)
                list_solution.append(curr_solution)
            if curr_solution["objectiveFunctionValue"] > solution["objectiveFunctionValue"]:
                solution = curr_solution
                new_solution = curr_solution
                ch = True
            else:
                new_solution = solution
        ch = True
        while ch == True:
            ch = False
            curr_solution = merge(solution, data_matrix)
            if curr_solution["objectiveFunctionValue"] > solution["objectiveFunctionValue"]:
                solution = curr_solution
                new_solution = curr_solution
                ch = True
            else:
                new_solution = solution
    return new_solution


def local_serch(solution, data_matrix):
    solution_after_relocate_machine = relocate_machine(solution, data_matrix)
    if solution_after_relocate_machine["objectiveFunctionValue"] > solution["objectiveFunctionValue"]:
        return local_serch(solution_after_relocate_machine, data_matrix)
    else:
        solution_after_relocate_detail = relocate_detail(solution, data_matrix)
        if solution_after_relocate_detail["objectiveFunctionValue"] > solution["objectiveFunctionValue"]:
            return local_serch(solution_after_relocate_detail, data_matrix)
    return solution


def divide(solution, data_matrix,i):
    cluster_to_divide_id = i
    cluster_to_divide = solution["clusters_dict"][cluster_to_divide_id]
    if len(cluster_to_divide["machines"]) == 1 or len(cluster_to_divide["details"]) == 1:
        return solution

    machine_id_to_divide = random.randint(1, len(cluster_to_divide["machines"]) - 1)
    detail_id_to_divide = random.randint(1, len(cluster_to_divide["details"]) - 1)
    machines_subcluster_first = set(list(cluster_to_divide["machines"])[:machine_id_to_divide])
    details_subcluster_first = set(list(cluster_to_divide["details"])[:detail_id_to_divide])
    first_new_cluster = {"machines": set(machines_subcluster_first), "details": set(details_subcluster_first),
                         "data_matrix": data_matrix}

    machines_subcluster_second = cluster_to_divide["machines"] - machines_subcluster_first

    details_subcluster_second = cluster_to_divide["details"] - details_subcluster_first

    second_new_cluster = {"machines": set(machines_subcluster_second), "details": set(details_subcluster_second),
                          "data_matrix": solution["clusters_dict"][0]["data_matrix"]}


    new_cluster_list = deepcopy(solution["clusters_dict"])
    new_cluster_list.pop(cluster_to_divide_id)
    new_cluster_list.extend([first_new_cluster, second_new_cluster])

    new_solution = dict()
    new_solution["clusters_dict"], new_solution["objectiveFunctionValue"], new_solution["numberOfClusters"] = Solution(
        new_cluster_list, solution["clusters_dict"][0]["data_matrix"])
    new_solution = local_serch(new_solution, data_matrix)
    return new_solution


def merge(solution, data_matrix,i,j):
    clusters_to_merge = [i,j]
    new_machines_subcluster = list(solution["clusters_dict"][clusters_to_merge[0]]["machines"]) + list(
        solution["clusters_dict"][clusters_to_merge[1]]["machines"])
    new_details_subcluster = list(solution["clusters_dict"][clusters_to_merge[0]]["details"]) + list(
        solution["clusters_dict"][
            clusters_to_merge[
                1]]["details"])

    newCluster = {"machines": set(new_machines_subcluster), "details": set(new_details_subcluster),
                  "data_matrix": data_matrix}

    new_clusters_list = deepcopy(solution["clusters_dict"])
    if clusters_to_merge[0] < clusters_to_merge[1]:
        new_clusters_list.pop(clusters_to_merge[1])
        new_clusters_list.pop(clusters_to_merge[0])
        new_clusters_list.append(newCluster)
    else:
        new_clusters_list.pop(clusters_to_merge[0])
        new_clusters_list.pop(clusters_to_merge[1])
        new_clusters_list.append(newCluster)

    new_solution = dict()
    new_solution["clusters_dict"], new_solution["objectiveFunctionValue"], new_solution["numberOfClusters"] = Solution(
        new_clusters_list, data_matrix)


    new_solution = local_serch(new_solution, data_matrix)
    return new_solution


def relocate_machine(solution, data_matrix):
    clusters_list = deepcopy(solution["clusters_dict"])
    clusters_pairs = []
    for i in range(len(clusters_list)):
        for j in range(len(clusters_list)):
            if i != j:
                clusters_pairs.append([i, j])
    solutions_list = [solution]
    for pair in clusters_pairs:
        cluster_id_1 = pair[0]
        cluster_id_2 = pair[1]
        solutions_list.extend(
            relocate_machine_helper(deepcopy(clusters_list), cluster_id_1, cluster_id_2, data_matrix))

    # max_dict = dict()
    # max_solutions = 0
    # for i in range(len(solutions_list)):
    #     if max_solutions < solutions_list[i]["objectiveFunctionValue"]:
    #         max_solutions = solutions_list[i]["objectiveFunctionValue"]
    #         max_dict = solutions_list[i]
    #
    # return max_dict




    return max(solutions_list, key=lambda x: x["objectiveFunctionValue"])


def relocate_machine_helper(clusters_list, cluster_id_from, cluster_id_to, data_matrix):
    inner_cluster_list = deepcopy(clusters_list)
    if cluster_id_to > cluster_id_from:
        cluster_to = inner_cluster_list.pop(cluster_id_to)
        cluster_from = inner_cluster_list.pop(cluster_id_from)
    else:
        cluster_from = inner_cluster_list.pop(cluster_id_from)
        cluster_to = inner_cluster_list.pop(cluster_id_to)
    solutions_list = []
    if len(cluster_from["machines"]) == 1:
        return solutions_list

    for machine_to_relocate in cluster_from["machines"]:
        buff_clusters_list = deepcopy(inner_cluster_list)

        new_cluster_from = {"machines": set((cluster_from["machines"] - {machine_to_relocate})),
                            "details": set(cluster_from["details"]),
                            "data_matrix": data_matrix}


        new_cluster_to = {"machines": set((cluster_to["machines"] | {machine_to_relocate})),
                          "details": set(cluster_to["details"]),
                          "data_matrix": data_matrix}


        buff_clusters_list.append(new_cluster_from)
        buff_clusters_list.append(new_cluster_to)
        new_solution = dict()
        new_solution["clusters_dict"], new_solution["objectiveFunctionValue"], new_solution[
            "numberOfClusters"] = Solution(buff_clusters_list, data_matrix)
        solutions_list.append(new_solution)
    return solutions_list


def relocate_detail(solution, data_matrix):
    clusters_list = deepcopy(solution["clusters_dict"])
    clusters_pairs = []
    for i in range(len(clusters_list)):
        for j in range(len(clusters_list)):
            if i != j:
                clusters_pairs.append([i, j])
    solutions_list = [solution]
    for pair in clusters_pairs:
        cluster_id_1 = pair[0]
        cluster_id_2 = pair[1]
        solutions_list.extend(relocate_detail_helper(deepcopy(clusters_list), cluster_id_1, cluster_id_2, data_matrix))
    return max(solutions_list, key=lambda x: x["objectiveFunctionValue"])



def relocate_detail_helper(clusters_list, cluster_id_from, cluster_id_to, data_matrix):
    inner_cluster_list = deepcopy(clusters_list)
    if cluster_id_to > cluster_id_from:
        cluster_to = inner_cluster_list.pop(cluster_id_to)
        cluster_from = inner_cluster_list.pop(cluster_id_from)
    else:
        cluster_from = inner_cluster_list.pop(cluster_id_from)
        cluster_to = inner_cluster_list.pop(cluster_id_to)

    solutions_list = []
    if len(cluster_from["details"]) == 1:
        return solutions_list
    for detail_to_relocate in cluster_from["details"]:
        buff_clusters_list = deepcopy(inner_cluster_list)

        new_cluster_from = {"machines": set(cluster_from["machines"]),
                            "details": set((cluster_from["details"] - {detail_to_relocate})),
                            "data_matrix": data_matrix}



        new_cluster_to = {"machines": set(cluster_to["machines"]),
                          "details": set((cluster_to["details"] | {detail_to_relocate})),
                          "data_matrix": data_matrix}


        buff_clusters_list.append(new_cluster_from)
        buff_clusters_list.append(new_cluster_to)

        new_solution = dict()
        new_solution["clusters_dict"], new_solution["objectiveFunctionValue"], new_solution[
            "numberOfClusters"] = Solution(buff_clusters_list, data_matrix)


        solutions_list.append(new_solution)
    return solutions_list
