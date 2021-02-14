import random
from copy import deepcopy

from solution import Solution

from main import print_solution


def get_initial_solution(data_matrix, machines_number, details_number):
    rand_machines = random.sample(range(1, machines_number), 10)
    rand_details = random.sample(range(1, details_number), 10)
    cluster_1 = {"machines": set(rand_machines), "details": set(rand_details), "data_matrix": data_matrix}

    # cluster_1 = Cluster(rand_machines, rand_details, data_matrix)
    other_machines = set(list(range(1, machines_number + 1))) - set(rand_machines)
    other_details = set(list(range(1, details_number + 1))) - set(rand_details)
    cluster_2 = {"machines": set(other_machines), "details": set(other_details), "data_matrix": data_matrix}
    # cluster_2 = Cluster(other_machines, other_details, data_matrix)
    init_solution = dict()
    init_solution["clusters_dict"], init_solution["cost"], init_solution[
        "numberOfClusters"] = Solution([cluster_1, cluster_2], data_matrix)
    return init_solution


def vns(data_matrix, machines_number, details_number):
    initial_solution = get_initial_solution(data_matrix, machines_number, details_number)
    # curr_solution = divide(initial_solution, data_matrix)

    curr_solution = local_serch(initial_solution, data_matrix)

    best_cost = 0.4801
    while best_cost > curr_solution["cost"]:
        shaking_result = shaking(curr_solution, data_matrix)
        new_solution = local_serch(shaking_result, data_matrix)
        if new_solution["cost"] > curr_solution["cost"]:
            curr_solution = new_solution
            print_solution(curr_solution, machines_number, details_number)
    return curr_solution

    return shaking_result



def shaking(solution, data_matrix):
    if len(solution["clusters_dict"]) == 1:
        new_solution = divide(solution, data_matrix)
    else:
        merge_or_divide = random.randint(0, 1)
        if merge_or_divide == 0:
            new_solution = divide(solution, data_matrix)
        else:
            new_solution = merge(solution, data_matrix)

        # new_solution = local_serch(solution, data_matrix)
        # while new_solution["cost"] > solution["cost"]:
        #     solution = new_solution
        #     new_solution = divide(new_solution, data_matrix)
        #     new_solution = local_serch(new_solution, data_matrix)
        # while new_solution["cost"] > solution["cost"]:
        #     solution = new_solution
        #     new_solution = merge(solution, data_matrix)
        #     new_solution = local_serch(new_solution, data_matrix)

    return new_solution


def local_serch(solution, data_matrix):
    solution_after_relocate_machine = relocate_machine(solution, data_matrix)
    if solution_after_relocate_machine["cost"] > solution["cost"]:
        return local_serch(solution_after_relocate_machine, data_matrix)
    else:
        solution_after_relocate_detail = relocate_detail(solution, data_matrix)
        if solution_after_relocate_detail["cost"] > solution["cost"]:
            return local_serch(solution_after_relocate_detail, data_matrix)
    return solution


def divide(solution, data_matrix):
    cluster_to_divide_id = random.randint(0, len(solution["clusters_dict"]) - 1)
    cluster_to_divide = solution["clusters_dict"][cluster_to_divide_id]
    if len(cluster_to_divide["machines"]) == 1 or len(cluster_to_divide["details"]) == 1:
        return solution

    machine_id_to_divide = random.randint(1, len(cluster_to_divide["machines"]) - 1)
    detail_id_to_divide = random.randint(1, len(cluster_to_divide["details"]) - 1)
    machines_subcluster_first = set(list(cluster_to_divide["machines"])[:machine_id_to_divide])
    details_subcluster_first = set(list(cluster_to_divide["details"])[:detail_id_to_divide])
    first_new_cluster = {"machines": set(machines_subcluster_first), "details": set(details_subcluster_first),
                         "data_matrix": data_matrix}
    # first_new_cluster = Cluster(machines_subcluster_first, details_subcluster_first, self.data_matrix)

    machines_subcluster_second = cluster_to_divide["machines"] - machines_subcluster_first

    details_subcluster_second = cluster_to_divide["details"] - details_subcluster_first

    second_new_cluster = {"machines": set(machines_subcluster_second), "details": set(details_subcluster_second),
                          "data_matrix": solution["clusters_dict"][0]["data_matrix"]}
    # second_new_cluster = Cluster(machines_subcluster_second, details_subcluster_second, self.data_matrix)

    new_cluster_list = deepcopy(solution["clusters_dict"])
    new_cluster_list.pop(cluster_to_divide_id)
    new_cluster_list.extend([first_new_cluster, second_new_cluster])

    new_solution = dict()
    new_solution["clusters_dict"], new_solution["cost"], new_solution["numberOfClusters"] = Solution(
        new_cluster_list, solution["clusters_dict"][0]["data_matrix"])
    # new_solution = Solution(new_cluster_list, self.data_matrix)
    return new_solution


def merge(solution, data_matrix):
    clusters_to_merge = random.sample(range(len(solution["clusters_dict"])), 2)
    new_machines_subcluster = list(solution["clusters_dict"][clusters_to_merge[0]]["machines"]) + list(
        solution["clusters_dict"][clusters_to_merge[1]]["machines"])
    new_details_subcluster = list(solution["clusters_dict"][clusters_to_merge[0]]["details"]) + list(
        solution["clusters_dict"][
            clusters_to_merge[
                1]]["details"])

    newCluster = {"machines": set(new_machines_subcluster), "details": set(new_details_subcluster),
                  "data_matrix": data_matrix}
    # newCluster = Cluster(new_machines_subcluster, new_details_subcluster, self.data_matrix)

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
    new_solution["clusters_dict"], new_solution["cost"], new_solution["numberOfClusters"] = Solution(
        new_clusters_list, data_matrix)

    # newSolution = Solution(new_clusters_list, self.data_matrix)
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
    return max(solutions_list, key=lambda x: x["cost"])


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
        new_solution["clusters_dict"], new_solution["cost"], new_solution[
            "numberOfClusters"] = Solution(buff_clusters_list, data_matrix)
        # new_solution = Solution(buff_clusters_list, solution.data_matrix)
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
    return max(solutions_list, key=lambda x: x["cost"])


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
        new_solution["clusters_dict"], new_solution["cost"], new_solution[
            "numberOfClusters"] = Solution(buff_clusters_list, data_matrix)

        solutions_list.append(new_solution)
    return solutions_list
