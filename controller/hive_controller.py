from typing import List

from base.base_observable import BaseObservable
from base.observer import Observer
from model.buzzness import Bee


class HiveController(BaseObservable, Observer):

    def __init__(self, hive):
        super().__init__()
        self.hive = hive
        self.path_to_flower = []

    def __add_nectar(self):
        for comb in self.hive.clist:
            if not comb.has_nectar:
                comb.has_nectar = True
                break
            else:
                continue

    def __spread_path(self, path : List):
        self.path_to_flower = path
        self.notify()

    def update(self, observable: BaseObservable) -> None:
        if isinstance(observable,Bee):
            if observable.inhive:
                if observable.hasNectar:
                    print(f"Bee {observable.ID} came back to hive with nectar")
                    observable.hasNectar = False
                    self.__add_nectar()
                    if len(observable.path_to_flower)>0:
                        self.__spread_path(observable.path_to_flower)


