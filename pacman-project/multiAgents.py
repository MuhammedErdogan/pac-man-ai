# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import random

import util
from util import manhattanDistance

from game import Agent, Directions


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction
          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
          The expectimax function returns a tuple of (actions,
        """
        "*** YOUR CODE HERE ***"
        action, value = self.expectimax(gameState, "", self.depth * gameState.getNumAgents(), 0)
        return action

    def expectimax(self, game_state, action, depth, agent_index):
        if game_state.isWin() or game_state.isLose() or depth == 0:
            return action, self.evaluationFunction(game_state)

        return self.max_value(game_state, action, depth, agent_index) if agent_index == 0 else self.exp_value(game_state, action, depth, agent_index)

    def max_value(self, game_state, action, depth, agent_index):
        bestAction = None
        bestValue = float("-inf")

        legalActions = game_state.getLegalActions(agent_index)

        for legalAction in legalActions:
            if legalAction == Directions.STOP:
                continue

            successor = game_state.generateSuccessor(agent_index, legalAction)
            decided_action = action if depth != self.depth * game_state.getNumAgents() else legalAction
            new_depth = depth - 1
            new_agent_index = (agent_index + 1) % game_state.getNumAgents()
            tempAction, tempValue = self.expectimax(successor, decided_action, new_depth, new_agent_index)

            if tempValue > bestValue:
                bestAction = tempAction
                bestValue = tempValue

        return bestAction, bestValue

    def exp_value(self, game_state, action, depth, agent_index):
        legalActions = game_state.getLegalActions(agent_index)

        averageScore = 0
        for legalAction in legalActions:
            if legalAction == Directions.STOP:
                continue

            successor = game_state.generateSuccessor(agent_index, legalAction)
            new_depth = depth - 1
            new_agent_index = (agent_index + 1) % game_state.getNumAgents()
            bestAction, bestValue = self.expectimax(successor, action, new_depth, new_agent_index)
            averageScore += bestValue * 1.0 / len(legalActions)
        return action, averageScore


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    evalScore = 0
    floatMax = 999999999

    if currentGameState.isLose():
        return -floatMax
    elif currentGameState.isWin():
        return floatMax

    pacmanPos = currentGameState.getPacmanPosition()

    foodlist = currentGameState.getFood().asList()
    capsuleList = currentGameState.getCapsules()

    scaredGhosts, activeGhosts = [], []
    ghosts = currentGameState.getGhostStates()
    for ghost in ghosts:
        if not ghost.scaredTimer:
            activeGhosts.append(ghost)
        else:
            scaredGhosts.append(ghost)

    distanceToClosestActiveGhost = floatMax
    for ghost in activeGhosts:
        distanceToClosestActiveGhost = min(distanceToClosestActiveGhost,
                                           manhattanDistance(pacmanPos, ghost.getPosition()))

    distanceToClosestScaredGhost = floatMax
    closestScaredGhost = None
    for ghost in scaredGhosts:
        distance = manhattanDistance(pacmanPos, ghost.getPosition())
        distanceToClosestScaredGhost = min(distanceToClosestScaredGhost, distance)
        if distanceToClosestScaredGhost == distance:
            closestScaredGhost = ghost

    numberOfCapsulesLeft = len(capsuleList)
    numberOfFoodsLeft = len(foodlist)
    distanceToClosestFood = min(map(lambda x: manhattanDistance(pacmanPos, x), foodlist))
    distanceToClosestCapsule = floatMax
    if numberOfCapsulesLeft != 0:
        distanceToClosestCapsule = min(map(lambda x: manhattanDistance(pacmanPos, x), capsuleList))

    mazeSize = currentGameState.getWalls().width * currentGameState.getWalls().height

    # OUR HEURISTIC

    # IF DISTANCE TO CLOSEST ACTIVE GHOST IS LESS THAN 1, THEN WE MUST AVOID IT
    if distanceToClosestActiveGhost <= 1:
        return -floatMax
    # IF DISTANCE TO CLOSEST SCARED GHOST IS LESS THAN 1, THEN WE MUST EAT IT
    if distanceToClosestScaredGhost <= 1 < closestScaredGhost.scaredTimer:
        return floatMax

    # IF MAZE SIZE IS SMALLER THAN 175
    if mazeSize <= 175:
        scoreMultiplier = 1
        numberOfFoodsLeftMultiplier = 10
        numberOfCapsulesLeftMultiplier = 100000
        distanceToClosestFoodMultiplier = 0.15
        distanceToClosestCapsuleMultiplier = 0.4
        distanceToClosestActiveGhostMultiplier = 1
        distanceToClosestScaredGhostMultiplier = 2
        numberOfScaredGhostMultiplier = 10000
    # IF MAZE SIZE IS LARGER THAN 225
    else:
        scoreMultiplier = 1
        numberOfFoodsLeftMultiplier = 10
        numberOfCapsulesLeftMultiplier = 100000
        distanceToClosestFoodMultiplier = 0.15
        distanceToClosestCapsuleMultiplier = 0.4
        distanceToClosestActiveGhostMultiplier = 10
        distanceToClosestScaredGhostMultiplier = 20
        numberOfScaredGhostMultiplier = 10000

    # IF THERE ARE NO ACTIVE GHOSTS, THEN THE DISTANCE TO THE CLOSEST ACTIVE GHOST IS NOT IMPORTANT AND
    if len(activeGhosts) == 0:
        distanceToClosestActiveGhostMultiplier = 0

    # IF THERE ARE NO SCARED GHOSTS, THEN THE DISTANCE TO THE CLOSEST SCARED GHOST IS NOT IMPORTANT
    if len(scaredGhosts) == 0:
        distanceToClosestScaredGhostMultiplier = 0
    else:
        numberOfCapsulesLeftMultiplier = 0

    # IF THERE ARE NO CAPSULES LEFT, THEN THE DISTANCE TO THE CLOSEST CAPSULE IS NOT IMPORTANT
    if numberOfCapsulesLeft == 0:
        distanceToClosestCapsuleMultiplier = 0

    # GET EVAL SCORE
    evalScore += (currentGameState.getScore() ** 2) * scoreMultiplier
    evalScore -= (distanceToClosestFood ** 2) * distanceToClosestFoodMultiplier
    evalScore -= (distanceToClosestCapsule ** 2) * distanceToClosestCapsuleMultiplier
    evalScore -= (1 / (distanceToClosestActiveGhost ** 2)) * distanceToClosestActiveGhostMultiplier
    evalScore -= (distanceToClosestScaredGhost ** 2) * distanceToClosestScaredGhostMultiplier
    evalScore -= (numberOfCapsulesLeft ** 2) * numberOfCapsulesLeftMultiplier
    evalScore -= (numberOfFoodsLeft ** 2) * numberOfFoodsLeftMultiplier
    evalScore -= len(scaredGhosts) ** 2 * numberOfScaredGhostMultiplier

    return evalScore


# Abbreviation
better = betterEvaluationFunction
