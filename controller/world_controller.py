import logging

from base.base_observable import BaseObservable
from base.observer import Observer
from model.buzzness import Bee
from model.world import PropertyType, Property, World
from utils.constants import VALID_MOVE

class WorldController(Observer, BaseObservable):

    def __init__(self, world, world_size=(50, 50)):
        super().__init__()
        self.world = world
        self.width, self.height = world_size
        self.beeObserver = Observer

    def __update_bee_moved(self, bee):
        bee_x, bee_y = bee.pos
        matched_property = None
        for property in self.world.properties:
            start_x = property.pos[0]
            start_y = property.pos[1]
            width = property.width
            height = property.height
            if (not bee.hasNectar) and start_x <= bee_x < start_x + width and start_y <= bee_y < start_y + height:
                print(f"Bee {bee.ID} match property {property.type}, {property.pos}")
                matched_property = property
                break

        if matched_property is None:
            return
            
        if matched_property.type == PropertyType.FLOWER and matched_property.has_nectar:
            print(f"Bee {bee.ID} match property {matched_property.type}, {matched_property.pos}, now coming back hive")
            matched_property.has_nectar = False
            bee.set_nectar_found()
        else:
            print(f"Bee {bee.ID} match preventions, find another way")
            bee.step_back()  # This will now mark the move as invalid instead of moving back

    def update(self, observable: BaseObservable) -> None:
        if isinstance(observable, Bee):
            if not observable.inhive:
                self.__update_bee_moved(observable)
