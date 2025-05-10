from typing import List

from base.base_observable import BaseObservable
from base.observer import Observer
from model.buzzness import Bee


class HiveController(BaseObservable, Observer):
    """
    [2.2 Hive Controller] Manages hive operations and bee interactions within the hive.
    
    This controller handles:
    - Nectar storage in hive combs
    - Path information sharing between bees
    - Bee state management when returning to hive
    
    Attributes:
        hive: The hive instance being controlled
        path_to_flower: List of coordinates representing the path to a flower
    """

    def __init__(self, hive):
        """
        Initialize the HiveController.
        
        Args:
            hive: The hive instance to control
        """
        super().__init__()
        self.hive = hive
        self.path_to_flower = []

    def __add_nectar(self):
        """
        [2.2.1 Nectar storage] Add nectar to an empty comb in the hive.
        
        This method:
        - Iterates through hive combs
        - Finds the first empty comb
        - Marks it as containing nectar
        """
        for comb in self.hive.clist:
            if not comb.has_nectar:
                comb.has_nectar = True
                break
            else:
                continue

    def __spread_path(self, path: List):
        """
        [2.2.2 Path information sharing] Share path information with other bees.
        
        This method:
        - Updates the stored path to flower
        - Notifies observers (other bees) about the new path
        
        Args:
            path: List of coordinates representing the path to a flower
        """
        self.path_to_flower = path
        self.notify()

    def update(self, observable: BaseObservable) -> None:
        """
        [2.2 Hive Controller] Handle bee updates when they return to the hive.
        
        This method:
        - Processes bees that return to the hive with nectar
        - Stores nectar in hive combs
        - Shares path information if available
        
        Args:
            observable: The observable object (Bee) that triggered the update
        """
        if isinstance(observable, Bee):
            if observable.inhive:
                if observable.hasNectar:
                    print(f"Bee {observable.ID} came back to hive with nectar")
                    observable.hasNectar = False
                    self.__add_nectar()
                    if len(observable.path_to_flower) > 0:
                        self.__spread_path(observable.path_to_flower)


