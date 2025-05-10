from enum import Enum
import numpy as np
from  matplotlib.patches import Rectangle

class PropertyType(Enum):
    """
    [1.2.1 Property] Enumeration of possible property types in the world.
    Each type has a unique numeric value for visualization.
    """
    FLOWER = 20  # Flower property that can contain nectar
    TREE = 22    # Tree property that acts as an obstacle
    HOUSE = 24   # House property that acts as an obstacle
    WATER = 26   # Water property that acts as an obstacle

class Property:
    """
    [1.2.1 Property] Represents a property in the world.
    
    Attributes:
        type (PropertyType): The type of property (FLOWER, TREE, etc.)
        pos (tuple): Position (x, y) of the property
        width (int): Width of the property
        height (int): Height of the property
        has_nectar (bool): Whether the property contains nectar (only for FLOWER type)
    """
    def __init__(self, type, pos, width, height, has_nectar):
        self.type = type
        self.pos = pos
        self.width = width
        self.height = height
        self.has_nectar = has_nectar

class World:
    """
    [1.2 World] Represents the simulation world containing properties and the hive.
    
    The world is a 2D grid where:
    - Properties (flowers, trees, etc.) can be placed
    - The hive has a specific position and size
    - The background has a default value of 5
    
    Attributes:
        properties (list): List of Property objects in the world
        hive_pos (tuple): Position and size of the hive (x, y, width, height)
        world (numpy.ndarray): 2D array representing the world grid
    """
    def __init__(self, hive_pos, world_size):
        self.properties = []
        self.hive_pos = hive_pos
        self.world = np.full(world_size, 5)  # Simple background value

    def add_property(self, property):
        """
        [1.2.1 Property] Add a property to the world.
        
        Args:
            property (Property): The property to add to the world
        """
        self.properties.append(property)
        