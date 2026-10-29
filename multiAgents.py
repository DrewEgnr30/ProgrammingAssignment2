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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
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
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
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
        remaining_food = len(newFood.asList())
        food_weight = -1
        food_manhattan_distances = [manhattanDistance(new_food, newPos) for new_food in newFood.asList()]
        closest_food = 0

        if(newFood.asList()):
            closest_food = min(food_manhattan_distances)
            if(closest_food != 0):
                closest_food = 1/ closest_food
            else:
                closest_food = 10

        food_distance_weight = 1

        ghost_distance_scared_times = [(manhattanDistance(ghost.getPosition(), newPos), ghost.scaredTimer) for ghost in newGhostStates]
        ghost_distance_weight = -2

        if ghost_distance_scared_times:
            closest_ghost = min(ghost_distance_scared_times, key=lambda item: item[0])

        if closest_ghost[0] != 0:
            closest_ghost_distance = 1 / closest_ghost[0]
            closest_ghost_scared_timer = closest_ghost[1]
        else:
            closest_ghost_distance = 50
            closest_ghost_scared_timer = 0

        if(closest_ghost[0] <= 2 and closest_ghost_scared_timer == 0):
            ghost_distance_weight = ghost_distance_weight * 2

        elif(closest_ghost[0] <= 2 and closest_ghost_scared_timer > 3):
            ghost_distance_weight = -ghost_distance_weight

        

        value = successorGameState.getScore() + remaining_food * food_weight + closest_food * food_distance_weight + closest_ghost_distance * ghost_distance_weight
        
        return value

def scoreEvaluationFunction(currentGameState: GameState):
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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def evaluateMinimax(self, gameState: GameState, agent_index: int, current_depth: int) -> float:

        if gameState.isWin():
            return self.evaluationFunction(gameState)

        if gameState.isLose():
            return self.evaluationFunction(gameState)

        if current_depth == self.depth:
            return self.evaluationFunction(gameState)

        legal_actions = gameState.getLegalActions(agent_index)

        if agent_index == 0:
            best_value = float('-inf')

            for action in legal_actions:
                successor = gameState.generateSuccessor(agent_index, action)

                next_agent = agent_index + 1
                next_depth = current_depth


                value = self.evaluateMinimax(successor, next_agent, next_depth)
                best_value = max(best_value, value)

            return best_value

        else:
            worst_value = float('inf')

            for action in legal_actions:
                successor = gameState.generateSuccessor(agent_index, action)

                next_agent = agent_index + 1
                next_depth = current_depth

                if next_agent == gameState.getNumAgents():
                    next_agent = 0
                    next_depth = current_depth + 1

                value = self.evaluateMinimax(successor, next_agent, next_depth)
                worst_value = min(worst_value, value)

            return worst_value

    def getAction(self, gameState: GameState):
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
        agent_number = gameState.getNumAgents()
        pacman_agent_number = 0
        next_agent = pacman_agent_number + 1
        next_depth = 0
        legal_actions = gameState.getLegalActions(pacman_agent_number)
        best_action = legal_actions[0]
        best_value = float('-inf')

        for action in legal_actions:
            successor = gameState.generateSuccessor(pacman_agent_number, action)

            value = self.evaluateMinimax(successor, next_agent, next_depth)

            if(value > best_value):
                best_value = value
                best_action = action

        return best_action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def evaluateMinimaxPruning(self, gameState: GameState, agent_index: int, current_depth: int, alpha: float, beta: float) -> float:

        if gameState.isWin():
            return self.evaluationFunction(gameState)

        if gameState.isLose():
            return self.evaluationFunction(gameState)

        if current_depth == self.depth:
            return self.evaluationFunction(gameState)

        legal_actions = gameState.getLegalActions(agent_index)

        if agent_index == 0:
            best_value = float('-inf')

            for action in legal_actions:
                successor = gameState.generateSuccessor(agent_index, action)

                next_agent = agent_index + 1
                next_depth = current_depth


                value = self.evaluateMinimaxPruning(successor, next_agent, next_depth, alpha, beta)
                best_value = max(best_value, value)
                alpha = max(alpha, best_value)
                if alpha > beta:
                    break

            return best_value

        else:
            worst_value = float('inf')

            for action in legal_actions:
                successor = gameState.generateSuccessor(agent_index, action)

                next_agent = agent_index + 1
                next_depth = current_depth

                if next_agent == gameState.getNumAgents():
                    next_agent = 0
                    next_depth = current_depth + 1

                value = self.evaluateMinimaxPruning(successor, next_agent, next_depth, alpha, beta)
                worst_value = min(worst_value, value)
                beta = min(worst_value, beta)
                if beta < alpha:
                    break

            return worst_value

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        pacman_agent_number = 0
        next_agent = pacman_agent_number + 1
        next_depth = 0
        legal_actions = gameState.getLegalActions(pacman_agent_number)
        best_action = legal_actions[0]
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        for action in legal_actions:
            successor = gameState.generateSuccessor(pacman_agent_number, action)

            value = self.evaluateMinimaxPruning(successor, next_agent, next_depth, alpha, beta)

            if(value > best_value):
                best_value = value
                best_action = action
                alpha = best_value

        return best_action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def evaluateExpectimax(self, gameState: GameState, agent_index: int, current_depth: int) -> float:

        if gameState.isWin():
            return self.evaluationFunction(gameState)

        if gameState.isLose():
            return self.evaluationFunction(gameState)

        if current_depth == self.depth:
            return self.evaluationFunction(gameState)

        legal_actions = gameState.getLegalActions(agent_index)

        if agent_index == 0:
            best_value = float('-inf')

            for action in legal_actions:
                successor = gameState.generateSuccessor(agent_index, action)

                next_agent = agent_index + 1
                next_depth = current_depth


                value = self.evaluateExpectimax(successor, next_agent, next_depth)
                best_value = max(best_value, value)

            return best_value

        else:
            agent_values: list[float] = []
            for action in legal_actions:
                successor = gameState.generateSuccessor(agent_index, action)

                next_agent = agent_index + 1
                next_depth = current_depth

                if next_agent == gameState.getNumAgents():
                    next_agent = 0
                    next_depth = current_depth + 1

                value = self.evaluateExpectimax(successor, next_agent, next_depth)
                agent_values.append(value)

            agent_expected_value = sum(agent_values) / len(agent_values)

            return agent_expected_value

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        pacman_agent_number = 0
        next_agent = pacman_agent_number + 1
        next_depth = 0
        legal_actions = gameState.getLegalActions(pacman_agent_number)
        best_action = legal_actions[0]
        best_value = float('-inf')

        for action in legal_actions:
            successor = gameState.generateSuccessor(pacman_agent_number, action)

            value = self.evaluateExpectimax(successor, next_agent, next_depth)

            if(value > best_value):
                best_value = value
                best_action = action

        return best_action

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    """Weights"""
    remaining_food_weight = -1
    closest_food_weight = 1
    ghost_weight = -2
    end_state_reward = 0

    current_position = currentGameState.getPacmanPosition()
    ghost_states = currentGameState.getGhostStates()
    current_food_list = currentGameState.getFood().asList()
    current_food_amount = len(current_food_list)
    closest_food = 0

    food_manhattan_distances = [manhattanDistance(current_position, food) for food in current_food_list]

    if food_manhattan_distances:
        closest_food = min(food_manhattan_distances)

    if closest_food > 0:
        closest_food = 1/closest_food
    else:
        closest_food = 10

    ghost_manhattan_distance_timer_tuple = [{"distance": manhattanDistance(current_position, ghost.getPosition()) , "timer": ghost.scaredTimer} for ghost in ghost_states]

    ghost_value = 0

    for ghost in ghost_manhattan_distance_timer_tuple:

        ghost_distance = ghost["distance"]
        ghost_timer = ghost["timer"]

        if ghost_distance == 0:
            if ghost_timer > 0:
                ghost_value = ghost_value + 5
            else:
                ghost_value = ghost_value - 5

        elif ghost_distance > 0 and ghost_distance <= 2:
            if ghost_timer == 0:
                ghost_value = ghost_value + 1 / ghost_distance * 2 * ghost_weight
            elif ghost_timer > 3:
                ghost_value = ghost_value + 1 / ghost_distance * -ghost_weight

        else:
            ghost_value = ghost_value + 1 / ghost_distance * ghost_weight


    if currentGameState.isWin():
        end_state_reward = 100

    if currentGameState.isLose():
        end_state_reward = -100

    value = end_state_reward + currentGameState.getScore() + current_food_amount * remaining_food_weight + closest_food * closest_food_weight + ghost_value


    return value

# Abbreviation
better = betterEvaluationFunction
