import numpy as np

class Comb:
    """
    [1.3.1 Comb] A single comb cell in the hive.
    
    Attributes:
        pos (tuple): Position (row, col) of the comb in the hive
        has_nectar (bool): Whether the comb contains nectar
    """
    def __init__(self, pos):
        self.pos = pos
        self.has_nectar = False

class Hive:
    """
    [1.3 Hive] Represents the bee hive structure.
    
    Attributes:
        hive (numpy.ndarray): 2D array representing the hive grid
        clist (list): List of Combs in the hive
    """
    def __init__(self, hive_size):
        # Initialize the hive grid with default value 10
        self.hive = np.full(hive_size, 10)
        self.clist = []
        
        # Create Comb objects for each position in the grid
        for row in range(self.hive.shape[0]):
            for col in range(self.hive.shape[1]):
                self.clist.append(Comb((row, col)))