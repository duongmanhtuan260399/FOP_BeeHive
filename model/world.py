from enum import Enum
import numpy as np
from  matplotlib.patches import Rectangle

class PropertyType(Enum):
    FLOWER = 2 * (50/20)
    TREE = 4 * (50/20)
    HOUSE = 6 * (50/20)
    WATER = 8 * (50/20)

class Property:
    def __init__(self,type,pos,width,height,has_nectar):
        self.type = type
        self.pos = pos
        self.width = width
        self.height = height
        self.has_nectar = has_nectar

class World:
    WORLD_SIZE = (50,50)
    def __init__(self,hive_pos):
        self.properties = []
        self.hive_pos = hive_pos
        self.world = np.full(self.WORLD_SIZE,5*(50/20))

    def add_property(self,property):
        self.properties.append(property)
        