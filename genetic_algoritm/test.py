# import numpy
# from deap import base, algorithms
# from deap import creator
# from deap import tools
# import random
# import matplotlib.pyplot as plt
# import seaborn as sns
# """Решение OneMax"""
# "Подготовка"
# # константы задачи
# ONE_MAX_LENGTH = 100  # длина подлежащей оптимизации битовой строки
# # константы генетического алгоритма
# POPULATION_SIZE = 200  # количество индивидуумов в популяции
# P_CROSSOVER = 0.9  # вероятность скрещивания
# P_MUTATION = 0.1  # вероятность мутации индивидуума
# MAX_GENERATIONS = 50  # максимальное количество поколений
# HALL_OF_FAME_SIZE = 10
# RANDOM_SEED = 42
# random.seed(RANDOM_SEED)
#
# toolbox = base.Toolbox()
#
# toolbox.register("zeroOrOne", random.randint, 0, 1)
#
# creator.create("FitnessMax", base.Fitness, weights=(1.0,))
#
# creator.create("Individual", list, fitness=creator.FitnessMax)
# toolbox.register("individualCreator", tools.initRepeat,
#                  creator.Individual, toolbox.zeroOrOne, ONE_MAX_LENGTH)
#
# toolbox.register("populationCreator", tools.initRepeat,
#                  list, toolbox.individualCreator)
#
#
# def oneMaxFitness(individual):
#     return sum(individual),  # вернуть кортеж
#
# toolbox.register("evaluate", oneMaxFitness)
#
#
# "генетические операторы"
# toolbox.register("select", tools.selTournament, tournsize=3)
# toolbox.register("mate", tools.cxOnePoint)
# toolbox.register("mutate", tools.mutFlipBit, indpb=1.0/ONE_MAX_LENGTH)
#
# "Эволюция решения"
# def main():
#     population = toolbox.populationCreator(n=POPULATION_SIZE)
#     generationCounter = 0
#     fitnessValues = list(map(toolbox.evaluate, population))
#     for individual, fitnessValue in zip(population, fitnessValues):
#         individual.fitness.values = fitnessValue
#
#     fitnessValues = [individual.fitness.values[0] for individual in population]
#     maxFitnessValues = []
#     meanFitnessValues = []
#     while max(fitnessValues) < ONE_MAX_LENGTH and generationCounter < MAX_GENERATIONS:
#         generationCounter = generationCounter + 1
#
#         # турнирный отбор
#         offspring = toolbox.select(population, len(population))
#         #клонируем
#         offspring = list(map(toolbox.clone, offspring))
#         #скрещивание
#         for child1, child2 in zip(offspring[::2], offspring[1::2]):
#             if random.random() < P_CROSSOVER:
#                 toolbox.mate(child1, child2)
#             del child1.fitness.values
#             del child2.fitness.values
#         #мутация
#         for mutant in offspring:
#             if random.random() < P_MUTATION:
#                 toolbox.mutate(mutant)
#             del mutant.fitness.values
#
#         #Проверка индвидов к которым не приминялось скрещивание и мутация
#         freshIndividuals = [ind for ind in offspring if not ind.fitness.valid]
#         freshFitnessValues = list(map(toolbox.evaluate, freshIndividuals))
#         for individual, fitnessValue in zip(freshIndividuals, freshFitnessValues):
#             individual.fitness.values = fitnessValue
#         population[:] = offspring
#         fitnessValues = [ind.fitness.values[0] for ind in population]
#
#         # вычисляем максимальное и среднее значения, помещаем их
#         # в накопители и печатаем сводную информацию
#         maxFitness = max(fitnessValues)
#         meanFitness = sum(fitnessValues) / len(population)
#         maxFitnessValues.append(maxFitness)
#         meanFitnessValues.append(meanFitness)
#         print("- Поколение {}: Макс приспособ. = {}, Средняя приспособ. = {}"
#               .format(generationCounter, maxFitness, meanFitness))
#
#         # Лучший индивид
#         best_index = fitnessValues.index(max(fitnessValues))
#         print("Лучший индивидуум = ", *population[best_index], "\n")
#
#     plt.plot(maxFitnessValues, color='red')
#     plt.plot(meanFitnessValues, color='green')
#     plt.xlabel('Поколение')
#     plt.ylabel('Макс/средняя приспособленность')
#     plt.title('Зависимость максимальной и средней приспособленности от поколения')
#     plt.show()
#
# def main_1():
#
#     # create initial population (generation 0):
#     population = toolbox.populationCreator(n=POPULATION_SIZE)
#
#     # prepare the statistics object:
#     stats = tools.Statistics(lambda ind: ind.fitness.values)
#     stats.register("max", numpy.max)
#     stats.register("avg", numpy.mean)
#
#     # perform the Genetic Algorithm flow:
#     population, logbook = algorithms.eaSimple(population, toolbox, cxpb=P_CROSSOVER, mutpb=P_MUTATION, ngen=MAX_GENERATIONS,
#                                    stats=stats, verbose=True)
#
#
#     # Genetic Algorithm is done - extract statistics:
#     maxFitnessValues, meanFitnessValues = logbook.select("max", "avg")
#
#     # plot statistics:
#     sns.set_style("whitegrid")
#     plt.plot(maxFitnessValues, color='red')
#     plt.plot(meanFitnessValues, color='green')
#     plt.xlabel('Generation')
#     plt.ylabel('Max / Average Fitness')
#     plt.title('Max and Average Fitness over Generations')
#     plt.show()
#
# def main_2():
#
#     # create initial population (generation 0):
#     population = toolbox.populationCreator(n=POPULATION_SIZE)
#
#     # prepare the statistics object:
#     stats = tools.Statistics(lambda ind: ind.fitness.values)
#     stats.register("max", numpy.max)
#     stats.register("avg", numpy.mean)
#
#     # define the hall-of-fame object:
#     hof = tools.HallOfFame(HALL_OF_FAME_SIZE)
#
#     # perform the Genetic Algorithm flow with hof feature added:
#     population, logbook = algorithms.eaSimple(population, toolbox, cxpb=P_CROSSOVER, mutpb=P_MUTATION,
#                                               ngen=MAX_GENERATIONS, stats=stats, halloffame=hof, verbose=True)
#
#     # print Hall of Fame info:
#     print("Hall of Fame Individuals = ", *hof.items, sep="\n")
#     print("Best Ever Individual = ", hof.items[0])
#
#     # extract statistics:
#     maxFitnessValues, meanFitnessValues = logbook.select("max", "avg")
#
#     # plot statistics:
#     sns.set_style("whitegrid")
#     plt.plot(maxFitnessValues, color='red')
#     plt.plot(meanFitnessValues, color='green')
#     plt.xlabel('Generation')
#     plt.ylabel('Max / Average Fitness')
#     plt.title('Max and Average Fitness over Generations')
#
#     plt.show()
# main_2()