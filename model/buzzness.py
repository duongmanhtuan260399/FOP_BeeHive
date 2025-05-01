import random

class Bee:
    """
    Provides state and behaviour for worker bee in the simulation
    """

    def __init__(self, ID, pos, hive_pos, hive_size):
        """
        Initialise Bee object
        ID:  identifier for the bee
        pos: (x,y) position of bee
        age: set to zero at birth
        inhive: is the bee inside the hive, or out in the world?, True at birth
        """
        self.ID = ID
        self.pos = pos
        self.age = 0
        self.inhive = True
        self.hasNectar = False
        self.hive_pos = hive_pos
        self.hive_size = hive_size
        self.path_to_hive = []


    def step_change(self, subgrid=None):
        """
        Update Bee object on each timestep
        subgrid: gives view of surroundings for choosing where to move (not used for now)
        """
        if self.inhive and not self.hasNectar:
            validmoves = [(1,0), (0,1), (1,1)]
        elif len(self.path_to_hive) == 0:
            validmoves = [(1,0),(1,1),(-1,-1),(0,1),(-1,0),(0,-1),(-1,1),(1,-1)] # list of valid moves
        else:
            validmoves = [self.path_to_hive.pop(0)]
        move_x, move_y = random.choice(validmoves)
        new_x = self.pos[0] + move_x
        new_y = self.pos[1] + move_y
        if new_x > 0 and new_y > 0:
            self.pos = (new_x, new_y)
        if new_x > self.hive_size[0] or new_y > self.hive_size[1]:
            self.inhive = False
            self.pos = self.hive_pos
        else:
            self.inhive = True
            self.pos = self.hive_size


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
