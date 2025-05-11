import logging

from base.base_observable import BaseObservable
from base.observer import Observer
from model.buzzness import Bee
from model.world import PropertyType, Property, World
from utils.constants import VALID_MOVE

class WorldController(Observer, BaseObservable):
    """
    [2.1 World Controller] Manages interactions between bees and the world.
    
    Attributes:
        world (World): The world instance being controlled
        world_size (Tuple(int,int)): Size of the world
    """
    def __init__(self, world, world_size=(50, 50)):
        super().__init__()
        self.world = world
        self.width, self.height = world_size

    def _check_property_collision(self, bee_pos, property):
        """
        [2.1.1 Collision detection] Check if bee position collides with a property.
            
        Returns:
            bool: True if bee collides with property
        """
        bee_x, bee_y = bee_pos
        start_x, start_y = property.pos
        return (start_x <= bee_x < start_x + property.width and 
                start_y <= bee_y < start_y + property.height)

    def _handle_flower_interaction(self, bee, flower):
        """
        [2.1.2 Nectar collection] Handle bee interaction with a flower.
        """
        if flower.has_nectar:
            print(f"Bee {bee.ID} match property {flower.type}, {flower.pos}, now coming back hive")
            flower.has_nectar = False
            bee.set_nectar_found()
        else:
            print(f"Bee {bee.ID} found empty flower at {flower.pos}")

    def _handle_obstacle_interaction(self, bee, obstacle):
        """
        [2.1.1 Collision detection] Handle bee interaction with an obstacle.
        """
        print(f"Bee {bee.ID} match preventions, find another way")
        # Water obstacles require two step backs
        if obstacle.type == PropertyType.WATER:
            bee.step_back()
            bee.step_back()
        else:
            bee.step_back()

    def __update_bee_moved(self, bee):
        # Skip collision check if bee already has nectar
        if bee.hasNectar:
            return

        # Find the first property that the bee collides with
        for property in self.world.properties:
            if self._check_property_collision(bee.pos, property):
                print(f"Bee {bee.ID} match property {property.type}, {property.pos}")
                
                # Handle the collision based on property type
                if property.type == PropertyType.FLOWER:
                    self._handle_flower_interaction(bee, property)
                else:
                    self._handle_obstacle_interaction(bee, property)
                break

    def update(self, observable: BaseObservable) -> None:
        """
        update() when a bee moves to detect collision with flower and obstacle.
        """
        if isinstance(observable, Bee):
            if not observable.inhive:
                self.__update_bee_moved(observable)
