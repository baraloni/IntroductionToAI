from board import Board
from search import SearchProblem, ucs, Node, extract_actions
import util
import numpy as np
import sys


class BlokusFillProblem(SearchProblem):
    """
    A one-player Blokus game as a search problem.
    This problem is implemented for you. You should NOT change it!
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.expanded = 0

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        """
        state: Search state
        Returns True if and only if the state is a valid goal state
        """
        return not any(state.pieces[0])

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, 1) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)


#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################
class BlokusCornersProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.corners = [(0, board_h - 1), (board_w - 1, 0), (board_w - 1, board_h - 1)]
        self.expanded = 0

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        """
        Check that corners are filled
        """
        for (x, y) in self.corners:
            if state.get_position(x, y) == -1:
                return False
        return True

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        cost = 0
        for action in actions:
            cost += action.piece.get_num_tiles()
        return cost


def blokus_corners_heuristic(state, problem):
    """
    Your heuristic for the BlokusCornersProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come up
    with an admissible heuristic; almost all admissible heuristics will be consistent
    as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the other hand,
    inadmissible or inconsistent heuristics may find optimal solutions, so be careful.
    """
    unfilled_corners = 0
    for (x, y) in problem.corners[:-1]:
        if state.get_position(x, y) == -1:
            unfilled_corners += 1

    filled = np.argwhere(state.state != -1)
    if not filled.any():
        x_max, y_max = (-1, -1)
    else:
        x_max, y_max = np.amax(filled, axis=0)

    x, y = problem.corners[2]
    cost = 0
    if state.get_position(x, y) == -1:
        cost = max(x - x_max, y - y_max)
    return cost + unfilled_corners


class BlokusCoverProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=[(0, 0)]):
        self.targets = targets.copy()
        self.expanded = 0
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.corners = [(0, board_h - 1), (board_w - 1, 0), (board_w - 1, board_h - 1)]
        self.full_graph = self.get_full_graph()

    def get_full_graph(self):
        return []

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        for (x, y) in self.targets:
            if state.get_position(x, y) == -1:
                return False
        return True

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        cost = 0
        for action in actions:
            cost += action.piece.get_num_tiles()
        return cost


def blokus_cover_heuristic(state, problem):
    """
    heuristic for the cover problem: returns the number of uncovered targets(consistent).
    :param state: a Board object
    :param problem: the problem to search in
    :return: the estimated cost of solving the problem from this current state
    """
    cost = 0
    for (x, y) in problem.targets:
        if state.get_position(x, y) == -1:
            cost += 1
    return cost


class ClosestLocationSearch:
    """
    In this problem you have to cover all given positions on the board,
    but the objective is speed, not optimality.
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=(0, 0)):
        self.expanded = 0
        self.targets = targets.copy()
        self.starting_point = self.targets.remove(starting_point) if starting_point in self.targets else starting_point
        self.board = Board(board_w, board_h, 1, piece_list, self.starting_point)

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def solve(self):
        """
        This method should return a sequence of actions that covers all target locations on the board.
        This time we trade optimality for speed.
        Therefore, your agent should try and cover one target location at a time. Each time, aiming for the closest uncovered location.
        You may define helpful functions as you wish.

        Probably a good way to start, would be something like this --

        current_state = self.board.__copy__()
        backtrace = []

        while ....

            actions = set of actions that covers the closest uncovered target location
            add actions to backtrace

        return backtrace
        """
        current_state = self.board.__copy__()
        backtrace = list()
        start_locations = [self.starting_point]
        targets = self.targets.copy()
        rerun = False
        reruns = 0

        while targets:
            # each iteration search for coverage to the next
            if rerun:
                # we want to reset the search but do something different
                # hence we will keep the mode we got stuck in as the first
                # the new search
                if reruns == 2 * len(self.targets):
                    return []

                rerun = False
                current_state = self.board.__copy__()
                backtrace = list()
                start_locations = [self.starting_point]
            else:
                closest_target = find_closest(start_locations, targets)

            actions = self.cover_target_search(current_state, closest_target)
            backtrace.extend(actions)
            start_locations.append(closest_target)
            targets.remove(closest_target)

            for action in actions:
                current_state.add_move(0, action)
            if not np.any(actions):
                targets = self.targets.copy()
                rerun = True
                reruns += 1

        return backtrace

    def get_successors(self, state):
        """
        :param state: current state
        :return: the state's successors list
        """
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]


    def cover_target_search(self, start_state, target):
        # Find list of actions to cover target
        """
        Search the node that has the lowest combined cost and heuristic first.
        """
        fringe = util.PriorityQueueWithFunction(lambda x: x.cost)
        visited = dict()

        # add root to fringe
        state = start_state
        fringe.push(Node(state, None, None, 1))
        visited[state] = 0

        while not fringe.isEmpty():
            current_v = fringe.pop()
            if current_v.state.get_position(target[0], target[1]) != -1:
                return extract_actions(start_state, current_v)

            for (successor, action, step_cost) in self.get_successors(current_v.state):
                successor_g = visited[current_v.state] + step_cost
                if successor not in visited or successor_g < visited[successor]:
                    visited[successor] = successor_g
                    successor_h = 1 if successor.get_position(target[0], target[1]) == -1 else 0
                    fringe.push(Node(successor, current_v, action,  successor_g + successor_h))


def find_closest(start_locations, targets):
    """
    :param start_locations: list of board coordinates (tuples of ints)
    :param targets: list of board coordinates (tuples of ints)
    :return: closest target to one of the starting points
    """
    shortest_distance = sys.maxsize
    closest = None
    for target in targets:
        for location in start_locations:
            dist = util.manhattanDistance(target, location)
            if dist < shortest_distance:
                closest = target
                shortest_distance = dist
    return closest

 
class MiniContestSearch:
    """
    Implement your contest entry here
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=(0, 0)):
        self.targets = targets.copy()
        "*** YOUR CODE HERE ***"

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def solve(self):
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


