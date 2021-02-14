

def get_number_of_ones_and_zeroes_cluster(cluster):
    number_of_cells = len(cluster["machines"]) * len(cluster["details"])
    cluster["number_of_ones"] = 0
    for machine in cluster["machines"]:
        for detail in cluster["details"]:
            cluster["number_of_ones"] += cluster["data_matrix"][machine - 1, detail - 1]
    return cluster["number_of_ones"], number_of_cells - cluster["number_of_ones"]


def get_total_number_of_ones(matrix):
    return matrix.sum()


"""По формуле считаем эффективность"""
def get_value(total_ones,clusters):
        ones_clusters = 0
        zeros_clusters = 0
        for cluster in clusters:
            ones_clusters += cluster["ones_number"]
            zeros_clusters += cluster["zeros_number"]
        return ones_clusters / (total_ones + zeros_clusters)



def is_feasible_solution(clusters_list):
        #  each cluster must contain at least 1 machine and 1 detail
        for cluster in clusters_list:
            if len(cluster["machines"]) > 0 and len(cluster["machines"]) > 0:
                pass
            else:
                return False
        #  each machine must be assigned to exactly 1 cluster
        for cluster_1 in clusters_list:
            for cluster_2 in clusters_list:
                if cluster_1 != cluster_2:
                    if len(set(cluster_1["machines"]) & set(cluster_2["machines"])) > 0:
                        return False
        #  each detail must be assigned to exactly 1 cluster
        for cluster_1 in clusters_list:
            for cluster_2 in clusters_list:
                if cluster_1 != cluster_2:
                    if len(set(cluster_1["details"]) & set(cluster_2["details"])) > 0:
                        return False
        return True




def Solution(clusters_dict,matrix):
    """получение нулей и единиц для каждого кластера """
    for cluster_index in range(len(clusters_dict)):
        clusters_dict[cluster_index]["ones_number"], clusters_dict[cluster_index]["zeros_number"]=get_number_of_ones_and_zeroes_cluster(clusters_dict[cluster_index])

    total_ones = get_total_number_of_ones(matrix)

    cost = get_value(total_ones, clusters_dict)

    numberOfClusters = len(clusters_dict)

    is_feasible = is_feasible_solution(clusters_dict)
    assert is_feasible, "тильт"

    return clusters_dict, cost, numberOfClusters



