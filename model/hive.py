import numpy as np

class Comb:
    """
    [1.3.1 Comb] Represents a single comb cell in the hive.
    
    Each comb cell:
    - Has a specific position in the hive grid
    - Can store nectar
    - Is part of the larger hive structure
    
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
    
    The hive is a 2D grid where:
    - Each cell is represented by a Comb object
    - The background has a default value of 10
    - Combs are arranged in a grid pattern
    
    Attributes:
        hive (numpy.ndarray): 2D array representing the hive grid
        clist (list): List of Comb objects in the hive
    """
    def __init__(self, hive_size):
        # Initialize the hive grid with default value 10
        self.hive = np.full(hive_size, 10)
        self.clist = []
        
        # Create Comb objects for each position in the grid
        for row in range(self.hive.shape[0]):
            for col in range(self.hive.shape[1]):
                self.clist.append(Comb((row, col)))