import random
import subprocess

import numpy as np


params = [5.07, 23.48, 96.92, 7.43, 9.45, 24.37, 38.68]
scoreMultiplier = params[0]
numberOfFoodsLeftMultiplier = params[1]
numberOfCapsulesLeftMultiplier = params[2]
distanceToClosestFoodMultiplier = params[3]
distanceToClosestCapsuleMultiplier = params[4]
distanceToClosestActiveGhostMultiplier = params[5]
distanceToClosestScaredGhostMultiplier = params[6]

popSize = 2

class Individual:
    def __init__(self, params):
        self.score = 0
        self.win_rate = ""
        self.params = params
        self.fitness = self.calculate_fitness()

    def __str__(self):
        return f"Score: {self.score} Win Rate: {self.win_rate} Individual: {self.params}"

    def calculate_fitness(self):
        self.score, self.win_rate = run_game(self)
        return self.score


def crossover(individual1, individual2):
    crossover_point = random.randint(0, len(individual1) - 1)
    return individual1[:crossover_point] + individual2[crossover_point:]


def crossover_for_pop(population):
    next_generation = []
    total_fitness = sum([individual.fitness for individual in population])
    weighted_selection = [(0.01 if individual.fitness < 0 else individual.fitness) / total_fitness for individual in
                          population]
    for _ in range(0, popSize):
        draw2 = np.random.choice(population, 2, p=weighted_selection)
        next_generation.append(Individual(crossover(draw2[0].params, draw2[1].params)))
    return next_generation


def mutation(individual):
    individual.params[random.randint(0, len(individual.params) - 1)] = return_float_between_1_and_100()
    individual.fitness = individual.calculate_fitness()
    return individual


def populate_population():
    return [Individual([return_float_between_1_and_100() for _ in range(7)]) for _ in range(popSize)]


def best_individual(population):
    return max(population, key=lambda individual: individual.fitness)


def decimal_range():
    start = float(1.0)
    stop = float(100.0)
    increment = float(1)
    while start < stop:
        yield start
        start += increment


def return_float_between_1_and_100():
    return float(random.random() * 999.9 + 0.1).__round__(2)


def run_game(individual):
    game_count = 2

    scoreMultiplier = individual.params[0]
    numberOfFoodsLeftMultiplier = individual.params[1]
    numberOfCapsulesLeftMultiplier = individual.params[2]
    distanceToClosestFoodMultiplier = individual.params[3]
    distanceToClosestCapsuleMultiplier = individual.params[4]
    distanceToClosestActiveGhostMultiplier = individual.params[5]
    distanceToClosestScaredGhostMultiplier = individual.params[6]

    returned_output = subprocess.check_output(
        f"python3 pacman.py -l smallClassic -p ExpectimaxAgent -a evalFn=better -q -n {game_count}",
        shell=True)
    returned_output = returned_output.decode("utf-8")
    score = float(returned_output.split("\n")[game_count].split(":")[1].strip())
    win_rate = returned_output.split("Win Rate: ")[1].split("%")[0].split("\n")[0].strip()

    return score, win_rate


if __name__ == '__main__':
    best_ind = None

    population = populate_population()
    for generation in range(50):
        print("\nGeneration: " + str(generation))
        best_ind = best_individual(population)
        print("\nBest Score: " + str(best_ind.score))
        print("Best Individual: " + str(best_ind.params))
        print("Win Rate: " + str(best_ind.win_rate))
        new_population = []
        crossover_pop = crossover_for_pop(population)
        crossover_pop.sort(key=lambda x: x.fitness, reverse=False)

        for _ in range(popSize):
            current = population[_]
            next_individual = mutation(crossover_pop[_])

            while True:
                if next_individual.fitness > current.fitness:
                    new_population.append(next_individual)
                    break
                else:
                    if random.random() < 0.01:
                        new_population.append(next_individual)
                        break
                    else:
                        new_population.append(current)
                        break

        population = new_population
        population.sort(key=lambda x: x.fitness, reverse=True)

    print("Best Score: " + str(best_ind.score))
    print("Best Individual: " + str(best_ind.params))
    print("Win Rate: " + str(best_ind.win_rate))
