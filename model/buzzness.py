import random
from enum import Enum
from utils.constants import VALID_MOVE, MOVE_FORWARD
from base.base_observable import BaseObservable
from base.observer import Observer
from utils.utils import Move, find_path_to_flower, find_path_to_hive


class BeeState(Enum):
    """
    [1.1.1 State Management] Enumeration of possible states for a bee in the simulation.
    
    States:
        WANDERING: Bee is exploring the world randomly
        FOLLOWING: Bee is following a known path to a flower
        RETURNING: Bee is returning to the hive with nectar
    """
    WANDERING = 1
    FOLLOWING = 2
    RETURNING = 3


class Bee(BaseObservable, Observer):
    """
    [1.1 Bee] Represents a worker bee in the simulation with its behavior and state management.
    
    The bee can:
    - Move around the world
    - Collect nectar from flowers
    - Return to the hive
    - Share information with other bees
    - Manage its energy levels
    
    Attributes:
        ID (int): Unique identifier for the bee
        pos (tuple): Current (x,y) position in the world
        age (int): Age of the bee
        inhive (bool): Whether the bee is inside the hive
        hasNectar (bool): Whether the bee is carrying nectar
        hive_pos (tuple): Position of the hive
        hive_size (tuple): Size of the hive
        world_size (tuple): Size of the world
        path_to_flower (list): Path to the nearest flower
        path_to_hive (list): Path back to the hive
        state (BeeState): Current state of the bee
        energy (int): Current energy level
        _move_invalid (bool): Flag for invalid moves
    """

    # [1.1.3 Energy Management] Constants for energy management
    MIN_ENERGY_TO_LEAVE = 50
    ENERGY_CHARGE_AMOUNT = 25
    ENERGY_CONSUMPTION = 1
    COMMUNICATION_THRESHOLD = 0.8

    def __init__(self, ID, pos, hive_pos, hive_size, world_size):
        """
        Initialize a new bee with default values and position.
        
        Args:
            ID (int): Unique identifier for the bee
            pos (tuple): Initial (x,y) position
            hive_pos (tuple): Position of the hive
            hive_size (tuple): Size of the hive
            world_size (tuple): Size of the world
        """
        super().__init__()
        self.ID = ID
        self.pos = pos
        self.age = 0
        self.inhive = True
        self.hasNectar = False
        self.hive_pos = hive_pos
        self.hive_size = hive_size
        self.world_size = world_size
        self.path_to_flower = []
        self.path_to_hive = []
        self.state = BeeState.WANDERING
        self.energy = 0
        self._move_invalid = False

    def _adjust_boundaries(self, x, y):
        """
        [1.1.2 Movement] Adjust coordinates to stay within world boundaries.
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
            
        Returns:
            tuple: Adjusted (x, y) coordinates
        """
        x = max(1, min(x, self.world_size[0] - 2))
        y = max(1, min(y, self.world_size[1] - 2))
        return (x, y)

    def _try_alternative_move(self, old_pos):
        """
        [1.1.2 Movement] Attempt to find an alternative move when the current move is invalid.
        
        Args:
            old_pos (tuple): The position before the invalid move
            
        Returns:
            bool: True if a valid alternative move was found, False otherwise
        """
        if self.energy <= 0:
            return False

        move = random.choice(VALID_MOVE)
        new_x, new_y = self._adjust_boundaries(
            old_pos[0] + move[0],
            old_pos[1] + move[1]
        )
            
        self.pos = (new_x, new_y)
        self.energy -= self.ENERGY_CONSUMPTION
        self.notify()
        
        if self._move_invalid:
            self.pos = old_pos
            self._move_invalid = False
            return self._try_alternative_move(old_pos)
            
        return True

    def _execute_move(self, move: Move) -> bool:
        """
        [1.1.2 Movement] Execute a move for the bee, handling boundaries and obstacles.
        
        Args:
            move (Move): The move to execute
            
        Returns:
            bool: True if the move was successful, False otherwise
        """
        new_x, new_y = self._adjust_boundaries(
            self.pos[0] + move[0],
            self.pos[1] + move[1]
        )
        
        old_pos = self.pos
        self.pos = (new_x, new_y)
        
        # Handle hive exit
        if self.inhive and (new_x >= self.hive_size[0] or new_y >= self.hive_size[1]):
            self.inhive = False
        
        self.notify()
        
        if self._move_invalid:
            if self.state == BeeState.WANDERING:
                self.pos = old_pos
                self._move_invalid = False
                return self._try_alternative_move(old_pos)
            else:
                self._move_invalid = False
                self.energy -= self.ENERGY_CONSUMPTION
                return True
        
        self.energy -= self.ENERGY_CONSUMPTION
        return True

    def _handle_hive_charging(self) -> bool:
        """
        [1.1.3 Energy Management] Handle energy charging when bee is in hive.
        
        Returns:
            bool: True if bee should continue moving, False if charging
        """
        if self.inhive and self.energy < self.MIN_ENERGY_TO_LEAVE:
            print(f"Bee {self.ID} is charging")
            self.energy += self.ENERGY_CHARGE_AMOUNT
            return False
        return True

    def _handle_hive_exit(self) -> bool:
        """
        [1.1.1 State Management] Handle bee exiting the hive.
        
        Returns:
            bool: True if bee exited hive, False otherwise
        """
        if (self.inhive and 
            (self.state == BeeState.WANDERING or self.state == BeeState.FOLLOWING) and 
            self.energy >= self.MIN_ENERGY_TO_LEAVE):
            
            print(f"Bee {self.ID} goes out the world")
            self.pos = (self.hive_pos[0], self.hive_pos[1])
            self.inhive = False
            
            if self.state == BeeState.WANDERING and self.path_to_flower:
                print(f"Bee {self.ID} stopped wandering because it has path to a flower with {len(self.path_to_flower)} steps")
                self.state = BeeState.FOLLOWING
            return True
        return False

    def _get_next_move(self) -> Move:
        """
        [1.1.1 State Management] Determine the next move based on current state.
        
        Returns:
            Move: The next move to execute
        """
        if self.state == BeeState.WANDERING:
            if not self.inhive and not self.hasNectar and self.energy <= 0:
                print(f"Bee {self.ID} out of energy, back to home")
                self.state = BeeState.RETURNING
                self.path_to_hive = find_path_to_hive((self.hive_pos[0], self.hive_pos[1]), self.pos)
                return None
            return random.choice(MOVE_FORWARD if self.ID == 1 else VALID_MOVE)
            
        elif self.state == BeeState.FOLLOWING:
            if not self.inhive and not self.hasNectar and not self.path_to_flower:
                print("Can't find a flower with pre-define path")
                self.state = BeeState.WANDERING
                return None
            print(f"Bee {self.ID} following the path, pop 1 step")
            return self.path_to_flower.pop(0)
            
        elif self.state == BeeState.RETURNING:
            if not self.path_to_hive:
                return None
            move = self.path_to_hive.pop(0)
            if not self.path_to_hive:
                print(f"Bee {self.ID} comes to hive")
                self.inhive = True
                self.pos = (0, 0)
                self.path_to_hive = []
                self.energy = 0
                self.state = BeeState.WANDERING
                self.notify()
            return move
            
        return None

    def step_change(self):
        """
        [1.1 Bee] Update the bee's state and position for each timestep.
        
        This method handles:
        - Energy management
        - State transitions
        - Movement decisions
        - Hive entry/exit
        
        Returns:
            bool: True if the bee moved, False otherwise
        """
        if not self._handle_hive_charging():
            return False
            
        if self._handle_hive_exit():
            return True

        move = self._get_next_move()
        if move is not None:
            return self._execute_move(move)
        return False

    def get_pos(self):
        """Get the current position of the bee."""
        return self.pos

    def get_inhive(self):
        """Check if the bee is inside the hive."""
        return self.inhive

    def set_inhive(self, value):
        """Set whether the bee is inside the hive."""
        self.inhive = value

    def get_nectar(self):
        """Check if the bee is carrying nectar."""
        return self.hasNectar

    def set_nectar(self, value):
        """Set whether the bee is carrying nectar."""
        self.hasNectar = value

    def set_nectar_found(self):
        """
        [1.1.4 Path finding] Update bee state when nectar is found.
        Sets paths to flower and hive, and changes state to RETURNING.
        """
        self.path_to_flower = find_path_to_flower((self.hive_pos[0], self.hive_pos[1]), self.pos)
        self.path_to_hive = find_path_to_hive((self.hive_pos[0], self.hive_pos[1]), self.pos)
        self.state = BeeState.RETURNING
        self.hasNectar = True
        self.inhive = False

    def step_back(self):
        """[1.1.2 Movement] Mark the last move as invalid, called by WorldController when bee hits an obstacle."""
        self._move_invalid = True

    def update(self, observable: BaseObservable) -> None:
        """
        [1.1.4 Path finding] Handle updates from observed objects (HiveController).
        
        Args:
            observable (BaseObservable): The object that triggered the update
        """
        from controller.hive_controller import HiveController
        from controller.world_controller import WorldController
        
        if isinstance(observable, HiveController):
            chance = random.uniform(0, 1)
            print(f"Bee {self.ID} receive path info with chance {chance} ")
            if chance > self.COMMUNICATION_THRESHOLD:
                if not self.path_to_flower or len(self.path_to_flower) >= len(observable.path_to_flower):
                    self.path_to_flower = observable.path_to_flower.copy()
                    print(f"Bee {self.ID} saved flower information with {len(self.path_to_flower)} steps")
            else:
                print(f"Bee {self.ID} did not receive flower information")

