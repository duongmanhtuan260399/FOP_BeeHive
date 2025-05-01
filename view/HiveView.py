class HiveView:
    def plot(self,hive,blist, ax):
        # plot the comb with levels
        if len(hive.clist) > 0:
            for comb in hive.clist:
                hive.hive[comb.pos[0], comb.pos[1]] = comb.level

        # plot the bees
        xvalues = [b.get_pos()[0] for b in blist if b.get_inhive()]
        yvalues = [b.get_pos()[1] for b in blist if b.get_inhive()]

        ax.imshow(hive.hive.T, origin="lower", cmap="YlOrBr")
        ax.scatter(xvalues, yvalues, color="yellow")
        ax.set_title("Bee Hive")
        ax.set_xlabel("X position")
        ax.set_ylabel("Y position")