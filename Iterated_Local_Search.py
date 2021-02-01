from func_ILS import*
import numpy as np
from numpy import sqrt


def perturbation(best):
    # используем 'double bridge move' для perturbation
    candidate = {"permutation": double_Bridge_Move(best["permutation"])}
    candidate["cost"] = total_length_Path(candidate["permutation"])
    return candidate


def local_Search(best):
    change = True
    while change:
        change = False
        candidate = {"permutation": stochastic_Two_Opt(best["permutation"],best["cost"])}
        candidate["cost"] = total_length_Path(candidate["permutation"])
        if candidate["cost"] < best["cost"]:
            change = True
            best = candidate

    return best

def construct_Initial_Solution(TSPLIB):
    # гриди
    n = len(TSPLIB)
    totalDistance = 0.0
    for index in range(n):
        if index == n - 1:
            point2 = TSPLIB[0]
        else:
            point2 = TSPLIB[index + 1]

        totalDistance += calculating_Distance(TSPLIB[index], point2)
    RW = []
    ib = random.randrange(0, n)
    M = np.zeros([n, n])
    for i in np.arange(0, n, 1):
        for j in np.arange(0, n, 1):
            if i != j:
                M[i, j] = sqrt((TSPLIB[i][0] - TSPLIB[j][0]) ** 2 + (TSPLIB[i][1] - TSPLIB[j][1]) ** 2)
            else:
                M[i, j] = float('inf')
    way = []
    way.append(ib)
    for i in np.arange(1, n, 1):
        s = []
        for j in np.arange(0, n, 1):
            s.append(M[way[i - 1], j])
        way.append(s.index(min(s)))
        for j in np.arange(0, i, 1):
            M[way[i], way[j]] = float('inf')
            M[way[i], way[j]] = float('inf')
    S = sum(
        [sqrt((TSPLIB[way[i]][0] - TSPLIB[way[i + 1]][0]) ** 2 + (TSPLIB[way[i]][1] - TSPLIB[way[i + 1]][1]) ** 2) for i
         in np.arange(0, n - 1, 1)]) + sqrt(
        (TSPLIB[way[n - 1]][0] - TSPLIB[way[0]][0]) ** 2 + (TSPLIB[way[n - 1]][1] - TSPLIB[way[0]][1]) ** 2)
    if S < totalDistance:
        totalDistance = S
        RW = way
    permutation =[]
    for i in range(len(RW)):
        permutation.append(TSPLIB[RW[i]])
    return permutation

#ппроверкааа
def acceptance_Criterion(best, candidate):
    if candidate["cost"] < best["cost"]:
        best = candidate

    return best

def search(points, max_Iterations):
    best = {"permutation": construct_Initial_Solution(points)}
    best["cost"] = total_length_Path(best["permutation"])
    # теперь уточните это с помощью локального поиска для получения локальных оптимумов
    best = local_Search(best)
    # Итерация
    while max_Iterations>0:
        candidate = perturbation(best)
        candidate = local_Search(candidate)
        best = acceptance_Criterion(best, candidate)
        max_Iterations-=1
    return best
