import random
import subprocess

scoreMultiplier = 1.0
numberOfFoodsLeftMultiplier = 1.0
numberOfCapsulesLeftMultiplier = 1.0
distanceToClosestFoodMultiplier = 1.0
distanceToClosestCapsuleMultiplier = 1.0
distanceToClosestActiveGhostMultiplier = 1.0
distanceToClosestScaredGhostMultiplier = 1.0


def decimal_range():
    start = float(1.0)
    stop = float(100.0)
    increment = float(1)
    while start < stop:
        yield start
        start += increment


def return_float_between_1_and_100():
    return float(random.random() * 100.0 + 1.0).__round__(2)


if __name__ == '__main__':
    max_avg_score = 0
    max_avg_score_win_rate = ""
    max_avg_score_params = []

    game_count = 50

    for i in range(1000):
        print("Game Number: " + str(i+1))

        scoreMultiplier = return_float_between_1_and_100()
        numberOfFoodsLeftMultiplier = return_float_between_1_and_100()
        numberOfCapsulesLeftMultiplier = return_float_between_1_and_100()
        distanceToClosestFoodMultiplier = return_float_between_1_and_100()
        distanceToClosestCapsuleMultiplier = return_float_between_1_and_100()
        distanceToClosestActiveGhostMultiplier = return_float_between_1_and_100()
        distanceToClosestScaredGhostMultiplier = return_float_between_1_and_100()

        returned_output = subprocess.check_output(
            f"python3 pacman.py -l smallClassic -p ExpectimaxAgent -a evalFn=better -q -n {game_count}",
            shell=True)
        returned_output = returned_output.decode("utf-8")
        score = float(returned_output.split("\n")[game_count].split(":")[1].strip())
        win_rate = returned_output.split("Win Rate: ")[1].split("%")[0].split("\n")[0].strip()

        if score > max_avg_score:
            max_avg_score = score
            max_avg_score_win_rate = win_rate
            max_avg_score_params = [scoreMultiplier,
                                    numberOfFoodsLeftMultiplier,
                                    numberOfCapsulesLeftMultiplier,
                                    distanceToClosestFoodMultiplier,
                                    distanceToClosestCapsuleMultiplier,
                                    distanceToClosestActiveGhostMultiplier,
                                    distanceToClosestScaredGhostMultiplier]
            print('Max Avg Score: ', max_avg_score)
            print('Max Avg Score Win Rate: ', max_avg_score_win_rate)
            print('Max Avg Score Params: ', max_avg_score_params)

    print('Max Avg Score: ', max_avg_score)
    print('Max Avg Score Win Rate: ', max_avg_score_win_rate)
    print('Max Avg Score Params: ', max_avg_score_params)
