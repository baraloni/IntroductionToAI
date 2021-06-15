"""
In search.py, you will implement generic search algorithms
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()

class Node:
    """
    A node for the graphs built during the search
    """

    def __init__(self, state, parent, action, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost


def extract_actions(start_state, current):
    """
    :param start_state: the start state we need to and the backtrace at
    :param current: the state to back trace actions from
    :return: list of actions from start_state to current
    """
    actions = list()
    while not current.state == start_state:
        actions.append(current.action)
        current = current.parent
    return actions[::-1]

def generic_search_uc(problem, fringe):
    """
    generic search for bfs, dfs
    :param problem: the problem
    :param fringe: empty data structure for holding the states
    :return: list of actions from the problem's initial state to a solution
    """
    visited = set()

    # add root to fringe
    state = problem.get_start_state()
    fringe.push(Node(state, None, None))

    while not fringe.isEmpty():
        current_v = fringe.pop()

        if problem.is_goal_state(current_v.state):
            return extract_actions(problem.get_start_state(), current_v)

        if current_v.state not in visited:
            # get successors and add to stack
            successors = problem.get_successors(current_v.state)
            for s in successors:
                v = Node(s[0], current_v, s[1])
                fringe.push(v)

            visited.add(current_v.state)

def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    # """
    return generic_search_uc(problem, util.Stack())


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    return generic_search_uc(problem, util.Queue())


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    """
    return a_star_search(problem)


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    fringe = util.PriorityQueueWithFunction(lambda state: state.cost)
    visited = set()

    # add root to fringe
    root = problem.get_start_state()
    fringe.push(Node(root, None, None))

    while not fringe.isEmpty():
        current = fringe.pop()

        if problem.is_goal_state(current.state):
            return extract_actions(problem.get_start_state(), current)

        if current.state not in visited:
            visited.add(current.state)

            for s in problem.get_successors(current.state):
                if s not in visited:
                    fringe.push(Node(s[0], current, s[1], current.cost + s[2] + heuristic(s[0], problem)))



# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
