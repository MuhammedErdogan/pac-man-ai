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
    stop = float(10.0)
    increment = float(0.5)
    while start < stop:
        yield start
        start += increment


if __name__ == '__main__':
    max_avg_score = 0
    max_avg_score_win_rate = ""
    max_avg_score_params = []

    game_count = 30

    for i in decimal_range():
        scoreMultiplier = i
        for j in decimal_range():
            numberOfFoodsLeftMultiplier = j
            for k in decimal_range():
                numberOfCapsulesLeftMultiplier = k
                for l in decimal_range():
                    distanceToClosestFoodMultiplier = l
                    for m in decimal_range():
                        distanceToClosestCapsuleMultiplier = m
                        for n in decimal_range():
                            distanceToClosestActiveGhostMultiplier = n
                            for o in decimal_range():
                                distanceToClosestScaredGhostMultiplier = o

                                returned_output = subprocess.check_output(
                                    f"python3 pacman.py -l smallClassic -p ExpectimaxAgent -a evalFn=better -q -n {game_count}",
                                    shell=True)
                                returned_output = returned_output.decode("utf-8")
                                score = float(returned_output.split("\n")[game_count].split(":")[1].strip())
                                win_rate = returned_output.split("Win Rate: ")[1].split("%")[0].split("\n")[0].strip()

                                if score > max_avg_score:
                                    max_avg_score = score
                                    max_avg_score_win_rate = win_rate
                                    max_avg_score_params = [scoreMultiplier, numberOfFoodsLeftMultiplier,
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
