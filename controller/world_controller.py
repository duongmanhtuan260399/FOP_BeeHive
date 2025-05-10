import logging

from base.base_observable import BaseObservable
from base.observer import Observer
from model.buzzness import Bee
from model.world import PropertyType, Property, World
from utils.constants import VALID_MOVE

class WorldController(Observer, BaseObservable):
    """
    [2.1 World Controller] Manages interactions between bees and the world environment.
    
    Attributes:
        world (World): The world instance being controlled
        width (int): Width of the world
        height (int): Height of the world
    """
    def __init__(self, world, world_size=(50, 50)):
        super().__init__()
        self.world = world
        self.width, self.height = world_size

    def _check_property_collision(self, bee_pos, property):
        """
        [2.1.1 Collision detection] Check if bee position collides with a property.
        
        Args:
            bee_pos (tuple): Bee's current position (x, y)
            property (Property): Property to check collision against
            
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
        
        Args:
            bee (Bee): The bee interacting with the flower
            flower (Property): The flower property
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
        
        Args:
            bee (Bee): The bee interacting with the obstacle
            obstacle (Property): The obstacle property
        """
        print(f"Bee {bee.ID} match preventions, find another way")
        # Water obstacles require two step backs
        if obstacle.type == PropertyType.WATER:
            bee.step_back()
            bee.step_back()
        else:
            bee.step_back()

    def __update_bee_moved(self, bee):
        """
        Handles bee movement and collision detection.
        
        This method:
        - Checks if bee has collided with any property
        - Determines the type of collision (flower, obstacle)
        - Triggers appropriate response based on collision type
        
        Args:
            bee (Bee): The bee that has moved
        """
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
        Observer pattern implementation.
        
        Updates the world state when a bee moves:
        - Only processes bees that are outside the hive
        - Triggers collision detection and response
        
        Args:
            observable (BaseObservable): The observable object (Bee) that triggered the update
        """
        if isinstance(observable, Bee):
            if not observable.inhive:
                self.__update_bee_moved(observable)
