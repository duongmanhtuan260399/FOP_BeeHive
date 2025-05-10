import logging

from base.base_observable import BaseObservable
from base.observer import Observer
from model.buzzness import Bee
from model.world import PropertyType, Property, World
from utils.constants import VALID_MOVE

class WorldController(Observer, BaseObservable):
    """
    [2.1 World Controller] Manages interactions between bees and the world environment.
    
    This controller:
    - Handles collision detection between bees and properties
    - Manages nectar collection from flowers
    - Controls bee movement and boundary interactions
    - Observes bee movements and updates world state accordingly
    
    Attributes:
        world (World): The world instance being controlled
        width (int): Width of the world
        height (int): Height of the world
        beeObserver (Observer): Observer for bee-related events
    """
    def __init__(self, world, world_size=(50, 50)):
        super().__init__()
        self.world = world
        self.width, self.height = world_size
        self.beeObserver = Observer

    def __update_bee_moved(self, bee):
        """
        [2.1.1 Collision detection] Handles bee movement and collision detection.
        
        This method:
        - Checks if bee has collided with any property
        - Determines the type of collision (flower, obstacle)
        - Triggers appropriate response based on collision type
        
        Args:
            bee (Bee): The bee that has moved
        """
        bee_x, bee_y = bee.pos
        matched_property = None
        
        # Check for collisions with all properties
        for property in self.world.properties:
            start_x = property.pos[0]
            start_y = property.pos[1]
            width = property.width
            height = property.height
            
            # [2.1.1 Collision detection] Check if bee is within property boundaries
            if (not bee.hasNectar) and start_x <= bee_x < start_x + width and start_y <= bee_y < start_y + height:
                print(f"Bee {bee.ID} match property {property.type}, {property.pos}")
                matched_property = property
                break

        if matched_property is None:
            return
            
        # [2.1.2 Nectar collection] Handle flower collision and nectar collection
        if matched_property.type == PropertyType.FLOWER and matched_property.has_nectar:
            print(f"Bee {bee.ID} match property {matched_property.type}, {matched_property.pos}, now coming back hive")
            matched_property.has_nectar = False
            bee.set_nectar_found()
        else:
            # [2.1.3 Boundary management] Handle obstacle collision
            print(f"Bee {bee.ID} match preventions, find another way")
            bee.step_back()  # This will now mark the move as invalid instead of moving back

    def update(self, observable: BaseObservable) -> None:
        """
        [2.1 World Controller] Observer pattern implementation.
        
        Updates the world state when a bee moves:
        - Only processes bees that are outside the hive
        - Triggers collision detection and response
        
        Args:
            observable (BaseObservable): The observable object (Bee) that triggered the update
        """
        if isinstance(observable, Bee):
            if not observable.inhive:
                self.__update_bee_moved(observable)
