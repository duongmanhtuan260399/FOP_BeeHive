import numpy as np

class Comb:
    def __init__(self, pos, level):
        self.pos = pos
        self.level = level

class Hive:
    def __init__(self, hive_size):
        self.hive = np.full(hive_size, 10)
        self.clist = []