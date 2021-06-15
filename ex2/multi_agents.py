import math
import random

import numpy as np
import abc
import util
from game import Agent, Action


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def get_action(self, game_state):
        """
        You do not need to change this method, but you're welcome to.

        get_action chooses among the best options according to the evaluation function.

        get_action takes a game_state and returns some Action.X for some X in the set {UP, DOWN, LEFT, RIGHT, STOP}
        """

        # Collect legal moves and successor states
        legal_moves = game_state.get_agent_legal_actions()

        # Choose one of the best actions
        scores = [self.evaluation_function(game_state, action) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = np.random.choice(best_indices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legal_moves[chosen_index]

    def evaluation_function(self, current_game_state, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (GameState.py) and returns a number, where higher numbers are better.

        """
        successor = current_game_state.generate_successor(action=action)
        weights = [9.76662064, 5.0062741, 3.32961317]

        columns_diffs = np.diff(successor.board, axis=0)
        rows_diffs = np.diff(successor.board, axis=1)
        board_size = successor.board.size

        columns_diffs = np.abs(columns_diffs)
        rows_diffs = np.abs(rows_diffs)

        smooth_score = (- np.sum(columns_diffs) - np.sum(rows_diffs)) / successor.max_tile
        merge_score = (2 * board_size) - (np.count_nonzero(rows_diffs) + np.count_nonzero(columns_diffs))
        zero_tiles_score = board_size - np.count_nonzero(successor.board)

        score = weights[0] * zero_tiles_score
        score += weights[1] * smooth_score
        score += weights[2] * merge_score
        return score


def score_evaluation_function(current_game_state):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return current_game_state.score


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinmaxAgent, AlphaBetaAgent & ExpectimaxAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evaluation_function='scoreEvaluationFunction', depth=2):
        self.evaluation_function = util.lookup(evaluation_function, globals())
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state):
        return


class MinmaxAgent(MultiAgentSearchAgent):
    def get_action(self, game_state):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        game_state.get_legal_actions(agent_index):
            Returns a list of legal actions for an agent
            agent_index=0 means our agent, the opponent is agent_index=1

        Action.STOP:
            The stop direction, which is always legal

        game_state.generate_successor(agent_index, action):
            Returns the successor game state after an agent takes an action
        """
        """*** YOUR CODE HERE ***"""
        action, value = self._minimax(game_state,  self.depth)
        return action

    def _minimax(self, game_state, depth, agent_index=0):
        # reached the depth we've defined or reached a final state:
        actions = game_state.get_legal_actions(agent_index)
        if (depth == 0) or (not actions):
            return Action.STOP, self.evaluation_function(game_state)

        if agent_index == 0:  # max player
            v = -math.inf
            a = None
            for action in actions:
                successor = game_state.generate_successor(agent_index=agent_index, action=action)
                a_of_candidate, v_candidate = self._minimax(successor, depth, agent_index=1)
                if v < v_candidate:
                    v = v_candidate
                    a = action
            return a, v

        else:  # min player
            v = math.inf
            a = None
            for action in actions:
                successor = game_state.generate_successor(agent_index=agent_index, action=action)
                a_candidate, v_candidate = self._minimax(successor, depth - 1, agent_index=0)
                if v > v_candidate:
                    v = v_candidate
                    a = a_candidate
            return a, v


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def alphaBetaEval(self, state, depth, alpha, beta, agent_index=0):
        """
        Starting with alpha -inifnity and beta +infinity
        """

        legal_moves = state.get_legal_actions(agent_index)
        if depth == 0 or not legal_moves:
            return Action.STOP, self.evaluation_function(state)

        action = None
        if agent_index == 0:
            # wants to maximize the score
            score = -math.inf
            for move in legal_moves:
                successor = state.generate_successor(agent_index=agent_index, action=move)
                last_action, score = self.alphaBetaEval(successor, depth, alpha, beta, agent_index=1)
                if score > alpha:
                    alpha = score
                    action = move
                if beta <= alpha:
                    break
            return action, score

        else:
            # minimize the score 
            score = math.inf
            for move in legal_moves:
                successor = state.generate_successor(agent_index=agent_index, action=move)
                last_action, score = self.alphaBetaEval(successor, depth - 1, alpha, beta, agent_index=0)
                if score < beta:
                    beta = score
                    action = move
                if beta <= alpha:
                    break
            return action, score

    def get_action(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        """*** YOUR CODE HERE ***"""
        action, score = self.alphaBetaEval(game_state, self.depth, -math.inf, math.inf)
        print(action)
        return action


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """

    def get_action(self, game_state):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        The opponent should be modeled as choosing uniformly at random from their
        legal moves.
        """
        """*** YOUR CODE HERE ***"""
        action, value = self._expectimax(game_state, self.depth)
        return action

    def _expectimax(self, game_state, depth, agent_index=0):
        # reached the depth we've defined or reached a final state:
        actions = game_state.get_legal_actions(agent_index)
        if (depth == 0) or (not actions):
            return Action.STOP, self.evaluation_function(game_state)

        if agent_index == 0:  # max player
            v = -math.inf
            a = None
            for action in actions:
                successor = game_state.generate_successor(agent_index=agent_index, action=action)
                a_of_candidate, v_candidate = self._expectimax(successor, depth, agent_index=1)
                if v < v_candidate:
                    v = v_candidate
                    a = action
            return a, v

        else:  # random adversary
            num_of_actions = len(actions)
            v = 0
            a = random.randint(0, len(actions) - 1)
            for action in actions:
                successor = game_state.generate_successor(agent_index=agent_index, action=action)
                v += 1.0/num_of_actions * self._expectimax(successor, depth - 1, agent_index=0)[1]
            return a, v


def better_evaluation_function(current_game_state):
    """
    Your extreme 2048 evaluation function (question 5).

    DESCRIPTION: the function uses a linear combination of:
    count of number of empty tiles in the board: as lower number of empty tiles hint that the game will soon end.
    monotonic rows: for each row, check if the tiles are monotonic
    """
    weights = [18.77208978, 5.68761107, 2.8728082]
    columns_diffs = np.diff(current_game_state.board, axis=0)
    rows_diffs = np.diff(current_game_state.board, axis=1)
    board_size = current_game_state.board.size

    columns_diffs = np.abs(columns_diffs)
    rows_diffs = np.abs(rows_diffs)

    smooth_score = (- np.sum(columns_diffs) - np.sum(rows_diffs)) / current_game_state.max_tile
    merge_score = (2 * board_size) - (np.count_nonzero(rows_diffs) + np.count_nonzero(columns_diffs))
    zero_tiles_score = board_size - np.count_nonzero(current_game_state.board)

    score = weights[0] * zero_tiles_score
    score += weights[1] * smooth_score
    score += weights[2] * merge_score
    return score 


# Abbreviation
better = better_evaluation_function
