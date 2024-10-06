from pacman_module.game import Agent, Directions
from pacman_module.util import PriorityQueue
from pacman_module.util import manhattanDistance


def key(state):
    return (
        state.getPacmanPosition(),
        state.getFood(),
        tuple(state.getCapsules())
    )


def forwardCost(state, current_capsules, initial_capsules):
    pacman_pos = state.getPacmanPosition()
    food_positions = state.getFood().asList()

    if not food_positions:
        return 0

    dist = max(manhattanDistance(pacman_pos, food_pos) for food_pos in food_positions)

    capsule = 100000 if len(current_capsules) < len(initial_capsules) else 0

    return dist + capsule


def backwardCost(path, current_capsules, initial_capsules):
    cost = len(path)
    
    missing_capsules = len(initial_capsules) - len(current_capsules)
    cost += missing_capsules * 100000 

    return cost


def estimatedCost(state, path, initial_capsules):
    current_capsules = state.getCapsules()
    return backwardCost(path, current_capsules, initial_capsules) + forwardCost(state, current_capsules ,initial_capsules)


class PacmanAgent(Agent):
    def __init__(self):
        super().__init__()
        self.moves = None

    def get_action(self, state):
        if self.moves is None:
            self.moves = self.astar(state)

        if self.moves:
            return self.moves.pop(0)
        else:
            return Directions.STOP

    def astar(self, state):
        fringe = PriorityQueue()
        initial_capsules = set(state.getCapsules())
        fringe.push((state, [], initial_capsules), 0)
        closed = set()

        while not fringe.isEmpty():
            _, (current_state, path, remaining_capsules) = fringe.pop()

            if current_state.isWin():
                return path

            current_key = key(current_state)

            if current_key in closed:
                continue

            closed.add(current_key)

            for successor, action in current_state.generatePacmanSuccessors():
                new_path = path + [action]
                new_capsules = set(successor.getCapsules())

                cost = estimatedCost(successor, new_path, initial_capsules)
                fringe.push((successor, new_path, new_capsules), cost)

        return []
