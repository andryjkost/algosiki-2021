from Iterated_Local_Search import*
# функция возврата id по координатам точки
def get_key(val):
    for key, value in initial_path.items():

        if val == value:
            key_1=key
            del initial_path[key]
            return key_1

    return "key doesn't exist"
# все точки в словаре, чтобы можно было построить путь по их id
initial_path = {}
# для алгоритма просто запишим список координат
initial_path_list = []
# считывыем данные из файла в initial_path
with open("ja_1000.txt") as file:
    for line in file:
        if ' ' in line:
            string = line.split()
            result = [int(item) for item in string]
            key, *value = result
            initial_path[key] = value
        else:
            # колличество точек
            kol_points = int(line)

# запись координат в лист
for i in range(1, kol_points+1):
    initial_path_list.append(initial_path[i])
# задаем переменные для алгоса
# основные итерации
maxIterations = 1000
result = search(initial_path_list, maxIterations)
final_path_id = []

for index in result["permutation"]:
    final_path_id.append(get_key(index))
for i in final_path_id:
    print(i,end=" ")
print("\n")
print(result["cost"])

