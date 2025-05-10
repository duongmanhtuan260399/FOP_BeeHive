from matplotlib.patches import Rectangle


class WorldView:
    def plot(self, world, blist, ax):
        # Reset the world to background value
        world.world.fill(5 * (50/20))
        
        # plot the properties
        for prop in world.properties:
            # Calculate the end positions
            end_x = min(prop.pos[0] + prop.width, world.world.shape[1])  # shape[1] for x dimension
            end_y = min(prop.pos[1] + prop.height, world.world.shape[0])  # shape[0] for y dimension
            
            # Ensure we don't go out of bounds
            start_x = max(0, prop.pos[0])
            start_y = max(0, prop.pos[1])
            
            # Set the property value
            value = prop.type.value // 2 if prop.has_nectar else prop.type.value
            value = value * (50/20)
            # Note: In numpy arrays, first index is y (rows), second index is x (columns)
            world.world[start_y:end_y, start_x:end_x] = value

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