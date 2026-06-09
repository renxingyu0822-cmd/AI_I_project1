# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions
from typing import List

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    from util import Stack

    start = problem.getStartState()
    if problem.isGoalState(start):
        return []

    fringe = Stack()
    fringe.push((start, []))
    visited = set()

    while not fringe.isEmpty():
        state, path = fringe.pop()
        if state in visited:
            continue
        visited.add(state)

        if problem.isGoalState(state):
            return path

        for successor, action, stepCost in problem.getSuccessors(state):
            if successor not in visited:
                fringe.push((successor, path + [action]))

    return []

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue

    start = problem.getStartState()
    if problem.isGoalState(start):
        return []

    fringe = Queue()
    fringe.push((start, []))
    visited = set()

    while not fringe.isEmpty():
        state, path = fringe.pop()
        if state in visited:
            continue
        visited.add(state)

        if problem.isGoalState(state):
            return path

        for successor, action, stepCost in problem.getSuccessors(state):
            if successor not in visited:
                fringe.push((successor, path + [action]))

    return []

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    from util import PriorityQueue

    startState = problem.getStartState()
    if problem.isGoalState(startState):
        return []

    # priority queue ordered by cumulative cost
    pq = PriorityQueue()
    pq.push((startState, [], 0), 0)
    # nodes whose optimal cost is finalized
    visited = set()

    while not pq.isEmpty():
        curr, actions, currCost = pq.pop()
        if curr in visited:
            continue

        visited.add(curr)

        if problem.isGoalState(curr):
            return actions

        for next_state, action, cost in problem.getSuccessors(curr):
            if next_state not in visited:
                total = currCost + cost  # cumulative cost as priority
                pq.push((next_state, actions + [action], total), total)

    return []

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    from util import PriorityQueue

    startState = problem.getStartState()
    if problem.isGoalState(startState):
        return []

    # priority = current xost + predicted cost
    pq = PriorityQueue()
    pq.push((startState, [], 0), heuristic(startState, problem))
    # tracks best known g
    visited = {}

    while not pq.isEmpty():
        curr, actions, g = pq.pop()

        # skip if we already processed this state
        if curr in visited and g >= visited[curr]:
            continue
        visited[curr] = g

        if problem.isGoalState(curr):
            return actions

        for next_state, action, cost in problem.getSuccessors(curr):
            new_g = g + cost
            # only enqueue if this path improves on the best known cost
            if next_state not in visited or new_g < visited[next_state]:
                f = new_g + heuristic(next_state, problem)  # f = current + predicted
                pq.push((next_state, actions + [action], new_g), f)

    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
