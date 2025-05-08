import numpy as np

class Comb:
    def __init__(self, pos):
        self.pos = pos
        self.has_nectar = False

class Hive:
    def __init__(self, hive_size):
        self.hive = np.full(hive_size, 10)
        self.clist = []
        for row in range(self.hive.shape[0]):
            for col in range(self.hive.shape[1]):
                self.clist.append(Comb((row,col)))