import math
from typing import Tuple, List
# Define Position type hint for clarity
Position = Tuple[int, int]
Move = Tuple[int, int]

def find_path(hive_pos: Position, flower_pos: Position) -> List[Move]:
    """
    Calculates a sequence of moves from hive_pos to flower_pos using VALID_MOVES.

    Args:
        hive_pos: A tuple (x, y) representing the starting hive position.
        flower_pos: A tuple (x, y) representing the target flower position.

    Returns:
        A list of moves (tuples from VALID_MOVES) representing the path.
        Returns an empty list if the start and end positions are the same.
    """
    # --- Input Validation (Optional but good practice) ---
    if not (isinstance(hive_pos, (tuple, list)) and len(hive_pos) == 2 and
            isinstance(flower_pos, (tuple, list)) and len(flower_pos) == 2):
        raise ValueError("Positions must be tuples or lists of length 2 (x, y)")
    if not all(isinstance(coord, int) for coord in hive_pos + flower_pos):
         raise ValueError("Coordinates must be integers")
    # Make positions mutable tuples for easier updates if needed (or use lists)
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
            # Depending on requirements, you might raise an error or return partial path
            raise RuntimeError("Pathfinding exceeded maximum iterations")
            # return path_moves # Or return the path found so far

        # Calculate the difference vector to the target
        dx = target_pos[0] - current_pos[0]
        dy = target_pos[1] - current_pos[1]

        # Determine the best move based on the direction vector signs
        # math.copysign(1, x) returns 1.0 with the sign of x, or 0.0 if x is 0
        # int() converts this to -1, 0, or 1
        move_x = int(math.copysign(1, dx)) if dx != 0 else 0
        move_y = int(math.copysign(1, dy)) if dy != 0 else 0

        # The chosen move is (move_x, move_y)
        chosen_move: Move = (move_x, move_y)

        # --- Verification (optional, as our logic guarantees it's valid) ---
        # if chosen_move not in VALID_MOVES and chosen_move != (0,0):
        #    # This condition should ideally never be met with the current logic
        #    raise ValueError(f"Calculated move {chosen_move} is not in VALID_MOVES")
        # If dx and dy are both 0, we should already be at the target and the loop condition handles this.

        # Apply the move to the current position
        current_pos[0] += chosen_move[0]
        current_pos[1] += chosen_move[1]

        print(f"Move added to list: {chosen_move}")
        # Record the move
        path_moves.append(chosen_move)

        # print(f"  Moved {chosen_move}, New position: {tuple(current_pos)}") # Optional debug print

        iterations += 1

    print(f"Path found with {len(path_moves)} moves.")
    return path_moves
