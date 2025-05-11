import math
from typing import Tuple, List
# Define Position type hint for clarity
Position = Tuple[int, int]
Move = Tuple[int, int]

def find_path_to_flower(hive_pos: Position, flower_pos: Position) -> List[Move]:
    """
    Calculates a sequence of moves from hive_pos to flower_pos using VALID_MOVES.

    Args:
        hive_pos: A tuple (x, y) representing the starting hive position.
        flower_pos: A tuple (x, y) representing the target flower position.

    Returns:
        A list of moves (tuples from VALID_MOVES) representing the path.
        Returns an empty list if the start and end positions are the same.
    """
    current_pos = list(hive_pos)
    target_pos = tuple(flower_pos) # Target remains constant

    path_moves: List[Move] = []

    print(f"Starting pathfinding from {tuple(current_pos)} to {target_pos}")

    # Use a loop that continues as long as we haven't reached the target
    # Add a safety break for potential infinite loops (though unlikely here)
    max_iterations = 10000
    iterations = 0

    while tuple(current_pos) != target_pos:
        if iterations >= max_iterations:
            print("Warning: Maximum iterations reached. Aborting pathfinding.")
            raise RuntimeError("Pathfinding exceeded maximum iterations")

        # Calculate the difference vector to the target
        dx = target_pos[0] - current_pos[0]
        dy = target_pos[1] - current_pos[1]

        # math.copysign(1, x) returns 1.0 with the sign of x, or 0.0 if x is 0
        # int() converts this to -1, 0, or 1
        move_x = int(math.copysign(1, dx)) if dx != 0 else 0
        move_y = int(math.copysign(1, dy)) if dy != 0 else 0

        chosen_move: Move = (move_x, move_y)

        # Apply the move to the current position
        current_pos[0] += chosen_move[0]
        current_pos[1] += chosen_move[1]

        print(f"Move added to list: {chosen_move}")
        path_moves.append(chosen_move)

        iterations += 1

    print(f"Path found with {len(path_moves)} moves.")
    return path_moves

def find_path_to_hive(hive_pos: Position, current_pos: Position) -> List[Move]:
    """
    Calculates a sequence of moves from current_pos to hive_pos using VALID_MOVES.

    Args:
        hive_pos: A tuple (x, y) representing the hive position.
        current_pos: A tuple (x, y) representing the bee current position.

    Returns:
        A list of moves (tuples from VALID_MOVES) representing the path.
        Returns an empty list if the start and end positions are the same.
    """
    current_pos = list(current_pos)
    target_pos = tuple(hive_pos) # Target remains constant

    path_moves: List[Move] = []

    print(f"Starting pathfinding from {tuple(current_pos)} to {target_pos}")

    # Use a loop that continues as long as we haven't reached the target
    # Add a safety break for potential infinite loops (though unlikely here)
    max_iterations = 10000
    iterations = 0

    while tuple(current_pos) != target_pos:
        if iterations >= max_iterations:
            print("Warning: Maximum iterations reached. Aborting pathfinding.")
            raise RuntimeError("Pathfinding exceeded maximum iterations")

        dx = target_pos[0] - current_pos[0]
        dy = target_pos[1] - current_pos[1]

        # math.copysign(1, x) returns 1.0 with the sign of x, or 0.0 if x is 0
        # int() converts this to -1, 0, or 1
        move_x = int(math.copysign(1, dx)) if dx != 0 else 0
        move_y = int(math.copysign(1, dy)) if dy != 0 else 0

        chosen_move: Move = (move_x, move_y)

        # Apply the move to the current position
        current_pos[0] += chosen_move[0]
        current_pos[1] += chosen_move[1]

        print(f"Move added to list: {chosen_move}")
        path_moves.append(chosen_move)

        iterations += 1

    print(f"Path found with {len(path_moves)} moves.")
    return path_moves
