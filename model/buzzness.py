import random
from enum import Enum
from utils.constants import VALID_MOVE, MOVE_FORWARD
from base.base_observable import BaseObservable
from base.observer import Observer
from utils.utils import Move, find_path_to_flower, find_path_to_hive


class BeeState(Enum):
    WANDERING = 1
    FOLLOWING = 2
    RETURNING = 3

class Bee(BaseObservable, Observer):
    """
    Provides state and behaviour for worker bee in the simulation
    """

    def __init__(self, ID, pos, hive_pos, hive_size, world_size):
        """
        Initialise Bee object
        ID:  identifier for the bee
        pos: (x,y) position of bee
        age: set to zero at birth
        inhive: is the bee inside the hive, or out in the world?, True at birth
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

    def __move(self,move:Move):
        new_x = self.pos[0] + move[0]
        new_y = self.pos[1] + move[1]
        if new_x > 0 and new_y > 0:
            self.pos = (new_x, new_y)
        if self.inhive and (new_x >= self.hive_size[0] or new_y >= self.hive_size[1]):
            self.inhive = False
            self.pos = (self.hive_pos[0]-1, self.hive_pos[1]-1)
        if (not self.inhive) and (new_x >= self.world_size[0] or new_y >= self.world_size[1]):
            self.inhive = False
            self.pos = (self.world_size[0]-1, self.world_size[1]-1)
        self.energy -=1
        self.notify()


    def step_change(self):
        """
        Update Bee object on each timestep
        """
        if self.inhive and self.energy < 50:
            print(f"Bee {self.ID} is charging")
            self.inhive = True
            self.energy += 25
            return False
        if self.inhive and (self.state == BeeState.WANDERING or self.state == BeeState.FOLLOWING) and self.energy >= 50:
            print(f"Bee {self.ID} goes out the world")
            self.pos = self.hive_pos
            self.inhive = False
            if self.state == BeeState.WANDERING and len(self.path_to_flower) >0:
                print(f"Bee {self.ID} stopped wandering because it has path to a flower with {len(self.path_to_flower)} steps")
                self.state = BeeState.FOLLOWING

        move = None
        if self.state == BeeState.WANDERING:
            if (not self.inhive) and (not self.hasNectar) and self.energy <= 0:
                print(f"Bee {self.ID} out of energy, back to home")
                self.state = BeeState.RETURNING
                self.path_to_hive = find_path_to_hive((self.hive_pos[0], self.hive_pos[1]), self.pos)
            else:
                if self.ID ==1:
                    move = random.choice(MOVE_FORWARD)
                else:
                    move = random.choice(VALID_MOVE)
        elif self.state == BeeState.FOLLOWING:
            if (not self.inhive) and (not self.hasNectar) and len(self.path_to_flower) <= 0:
                print("Can't find a flower with pre-define path")
                self.state = BeeState.WANDERING
            else:
                print(f"Bee {self.ID} following the path, pop 1 step")
                move = self.path_to_flower.pop(0)
        elif self.state == BeeState.RETURNING:
            if len(self.path_to_hive) >0:
                dx, dy = self.path_to_hive.pop(0)
                if len (self.path_to_hive) == 0:
                    print(f"Bee {self.ID} comes to hive")
                    self.inhive = True
                    self.pos = (0,0)
                    self.path_to_hive = []
                    self.energy = 0
                    self.state = BeeState.WANDERING
                    self.notify()
                else:
                    move = (dx,dy)

        if move is not None:
            self.__move(move)



    def get_pos(self):
        return self.pos

    def get_inhive(self):
        return self.inhive

    def set_inhive(self, value):
        self.inhive = value

    def get_nectar(self):
        return self.hasNectar

    def set_nectar(self, value):
        self.hasNectar = value

    def set_nectar_found(self):
        self.path_to_flower = find_path_to_flower((self.hive_pos[0], self.hive_pos[1]), self.pos)
        self.path_to_hive = find_path_to_hive((self.hive_pos[0], self.hive_pos[1]), self.pos)
        self.state = BeeState.RETURNING
        self.hasNectar = True
        self.inhive = False
    def step_back(self):
        self.__move((-1,-1))

    def update(self, observable: BaseObservable) -> None:
        from controller.hive_controller import HiveController
        from controller.world_controller import WorldController
        if isinstance(observable, HiveController):
            chance = random.uniform(0,1)
            print(f"Bee {self.ID} received flower information with chance {chance}")
            if chance > 0.8:
                if len(self.path_to_flower)==0 or len(self.path_to_flower) >= len (observable.path_to_flower):
                    self.path_to_flower = []
                    for item in observable.path_to_flower:
                        self.path_to_flower.append(item)
                    print(f"Bee {self.ID} saved flower information with {len(self.path_to_flower)} steps")

