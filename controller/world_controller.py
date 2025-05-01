from model.world import PropertyType, Property, World
from utils.constants import VALID_MOVE
from utils.utils import find_path


class WorldController:
    def __init__(self, world, world_size=(50, 50)):
        self.world = world
        self.width, self.height = world_size

    def update_bee_moved(self, bee):
        bee_x, bee_y = bee.pos
        matched_property = None
        for property in self.world.properties:
            start_x = property.pos[0]
            start_y = property.pos[1]
            width = property.width
            height = property.height
            if start_x <= bee_x < start_x + width and start_y <= bee_y < start_y + height:
                matched_property : Property = property
                break

        if matched_property is None:
            return
        if matched_property.type == PropertyType.FLOWER and matched_property.has_nectar:
            matched_property.has_nectar = False
            bee.hasNectar = True
            bee.inhive = False
            bee.path_to_hive = find_path(self.world.hive_pos, bee.pos)
