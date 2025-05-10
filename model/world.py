from enum import Enum
import numpy as np
from  matplotlib.patches import Rectangle

class PropertyType(Enum):
    FLOWER = 20
    TREE = 22
    HOUSE = 24
    WATER = 26

class Property:
    def __init__(self,type,pos,width,height,has_nectar):
        self.type = type
        self.pos = pos
        self.width = width
        self.height = height
        self.has_nectar = has_nectar

class World:
    def __init__(self,hive_pos, world_size):
        self.properties = []
        self.hive_pos = hive_pos
        self.world = np.full(world_size, 5)  # Simple background value

    def add_property(self,property):
        self.properties.append(property)
        