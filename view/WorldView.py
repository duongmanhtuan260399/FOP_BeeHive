from matplotlib.patches import Rectangle


class WorldView:
    def plot(self, world,blist, ax):
        # plot the properties
        for prop in world.properties:
            world.world[prop.pos[0]:prop.pos[0] + prop.height, prop.pos[1]:prop.pos[1] + prop.width] = prop.type.value
        # plot bee
        xvalues = [b.get_pos()[0] for b in blist if not b.get_inhive()]
        yvalues = [b.get_pos()[1] for b in blist if not b.get_inhive()]

        ax.imshow(world.world, origin="lower", cmap="tab20", vmin=0, vmax=50)
        ax.scatter(xvalues, yvalues, color="yellow")

        # plot the hive
        rect = Rectangle((world.hive_pos[0], world.hive_pos[1]), world.hive_pos[2], world.hive_pos[3])
        ax.add_patch(rect)
        ax.set_title("Property")
        ax.set_xlabel("X position")
        ax.set_ylabel("Y position")