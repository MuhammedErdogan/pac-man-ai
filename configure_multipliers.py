import random
import subprocess

import numpy as np

scoreMultiplier = 33.02
numberOfFoodsLeftMultiplier = 31.49
numberOfCapsulesLeftMultiplier = 67.5
distanceToClosestFoodMultiplier = 80.88
distanceToClosestCapsuleMultiplier = 70.62
distanceToClosestActiveGhostMultiplier = 57.5
distanceToClosestScaredGhostMultiplier = 25.37

popSize = 4
generation = 0


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
    weighted_selection = [(0 if individual.fitness < 0 else individual.fitness) / total_fitness for individual in population]
    for _ in range(0, popSize):
        draw2 = np.random.choice(population, 2, p=weighted_selection)
        next_generation.append(Individual(crossover(draw2[0].params, draw2[1].params)))
    return next_generation


def selection(population):
    return random.sample(population, 2)

def populate_population():
    population = []
    for _ in range(popSize):
        individual = Individual([return_float_between_1_and_100() for _ in range(7)])
        population.append(individual)
    return population


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
    return float(random.random() * 100.0 + 1.0).__round__(2)


def run_game(individual):
    game_count = 20

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
    for _ in range(10):
        print("\nGeneration: " + str(generation))
        best_ind = best_individual(population)
        print("\nBest Score: " + str(best_ind.score))
        print("Best Individual: " + str(best_ind.params))
        print("Win Rate: " + str(best_ind.win_rate))
        new_population = []
        crossover_pop = crossover_for_pop(population)
        crossover_pop.sort(key=lambda x: x.fitness, reverse=False)

        for k in range(popSize):
            current = population[k]
            next_chromosome = crossover_pop[k]

            while True:
                if next_chromosome.fitness > current.fitness:
                    new_population.append(next_chromosome)
                    break
                else:
                    if random.random() < 0.01:
                        new_population.append(next_chromosome)
                        break
                    else:
                        new_population.append(current)
                        break

        population = new_population
        generation += 1
        population.sort(key=lambda x: x.fitness, reverse=True)

    print("Best Score: " + str(best_ind.score))
    print("Best Individual: " + str(best_ind.params))
    print("Win Rate: " + str(best_ind.win_rate))
