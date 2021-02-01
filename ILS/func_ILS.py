import random, math
# Функция, которая удаляет два ребра и меняет последовательность между удаленными ребрами
def stochastic_Two_Opt(points,distance):
    result =[]
    for i in range(len(points)):
            for k in range(i, len(points)):
                result = points[:i] + points[i:k][::-1] + points[k:]
                if i == 0:
                   new_distance=distance
                elif i==len(points)-1:
                   new_distance=distance
                else:
                    new_distance = distance - calculating_Distance(points[i],points[i-1]) - calculating_Distance(points[k],points[k-1]) + calculating_Distance(points[k-1],points[i-1])+ calculating_Distance(points[i],points[k])
                if new_distance < distance:
                    distance = new_distance
                    points = result
    return result

# Функция, вычисляющая расстояние между двумя точками
def calculating_Distance(point_1, point_2):
    summ = 0.0
    for coord1, coord2 in zip(point_1, point_2):
        summ += pow((coord1 - coord2), 2)
    return math.sqrt(summ)


# Функция, которая вычисляет общую длину пути
def total_length_Path(points):
    total_Distance = 0.0
    size = len(points)
    for index in range(size):
        if index == size - 1:
            point2 = points[0]
        else:
            point2 = points[index + 1]
        total_Distance += calculating_Distance(points[index], point2)
    return total_Distance


# (a,b,c,d)-> (a,d,c,b)
def double_Bridge_Move(perm):
    # make 4 slices
    slice_Length = int(len(perm) / 4)
    p1 = 1 + random.randrange(0, slice_Length)
    p2 = p1 + 1 + random.randrange(0, slice_Length)
    p3 = p2 + 1 + random.randrange(0, slice_Length)
    return perm[0:p1] + perm[p3:] + perm[p2:p3] + perm[p1:p2]









