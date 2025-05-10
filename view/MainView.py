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
        hive_pos = (15,15,2,2)
        hive_size = (40, 40)
        world_size = (50, 50)

        world = World(hive_pos, world_size)
        self.read_property(config_file,world)
        world_controller = WorldController(world)

        hive = Hive(hive_size)
        hiveController = HiveController(hive)

        bees = []
        for i in range(num_bees):
            bee = Bee(i+1, (0, 0), (hive_pos[0], hive_pos[1]), hive_size, world_size)
            # Register observers
            bee.attach(world_controller)
            bee.attach(hiveController)

            # Register observable
            hiveController.attach(bee)
            world_controller.attach(bee)

            bees.append(bee)


        history = []
        if visualize:
            plt.ion()
            fig, axes = plt.subplots(1, 2, figsize=(10, 5))

        for t in range(1, time_steps + 1):
            for bee in bees:
                bee.step_change()
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
    main.simulate(time_steps=120,num_bees=5,config_file='properties.json',visualize=True)
