from typing import Tuple

from matplotlib import pyplot as plt

from controller.hive_controller import HiveController
from controller.world_controller import WorldController
from model.buzzness import Bee
from model.hive import Hive
from model.world import World, PropertyType, Property
from view.HiveView import HiveView
from view.WorldView import WorldView
import json


class MainView():
    def read_property(self,property_file,world):
        with open(property_file, 'r') as file:
            jsonFile = json.load(file)
        props = jsonFile.get("properties", {})
        # Loop over each property type and plot them with the specified colours.
        for prop_type, items in props.items():
            for item in items:
                x = item.get("x", 0)
                y = item.get("y", 0)
                width = item.get("width", 0)
                height = item.get("height", 0)
                if prop_type == "trees":
                    has_nectar = False
                    prop = PropertyType.TREE
                elif prop_type == "water":
                    has_nectar = False
                    prop = PropertyType.WATER
                elif prop_type == "house":
                    has_nectar = False
                    prop = PropertyType.HOUSE
                elif prop_type == "flower":
                    has_nectar = True
                    prop = PropertyType.FLOWER
                else:
                    value = None  # Fallback color in case other types are encountered
                world.add_property(Property(prop, (x, y), width, height, has_nectar))

    def simulate(self,time_steps, num_bees, config_file, visualize=True):
        hive_pos = (15,15,4,4)
        hive_size = (40, 40)
        bees = [Bee(i, (0,0),(hive_pos[0],hive_pos[1]),hive_size) for i in range(1,num_bees)]

        world = World(hive_pos)
        self.read_property(config_file,world)
        world_controller = WorldController(world)

        hive = Hive(hive_size)
        hiveController = HiveController(hive)
        history = []
        if visualize:
            plt.ion()
            fig, axes = plt.subplots(1, 2, figsize=(10, 5))

        for t in range(1, time_steps + 1):
            for bee in bees:
                bee.step_change()
                world_controller.update_bee_moved(bee)
                print(bee.pos)
            hiveController.update_comb_building()
#            history.append({'time': t, 'honey': world.hive.honey_storage, 'comb': world.hive.comb_built})
            if visualize:
                axes[0].clear()
                axes[1].clear()
                # use original plot_hive from task4.py
                hiveView = HiveView()
                hiveView.plot(hive,bees, ax=axes[0])

                worldView = WorldView()
                worldView.plot(world,bees, ax=axes[1])
                fig.suptitle(f"Timestep {t}")
                plt.pause(0.1)

        if visualize:
            plt.ioff()
            plt.show()
        return history

if __name__ == "__main__":
    main = MainView()
    main.simulate(time_steps=20,num_bees=20,config_file='properties.json',visualize=True)
