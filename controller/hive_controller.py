import numpy as np

from model.hive import Comb


class HiveController:
    def __init__(self, hive):
        self.hive = hive
        self.building_phase = False
        self.comb_build_timer = 0

    def update_comb_building(self):
        hive_grid = self.hive.hive

        total_combs = np.count_nonzero(hive_grid != 10)
        full_combs = np.count_nonzero(hive_grid == 5)

        if (total_combs > 0 and full_combs / total_combs >= 0.7) or total_combs == 0:
            self.building_phase = True

        if self.building_phase:
            self.comb_build_timer += 1
            if self.comb_build_timer >= 60:
                self.build_next_comb()
                self.comb_build_timer = 0

    def build_next_comb(self):
        hive_matrix = self.hive.hive
        rows, cols = hive_matrix.shape

        for i in range(rows):
            for j in range(cols):
                if hive_matrix[i, j] == 10:  # no comb yet
                    # Place new comb
                    hive_matrix[i, j] = 0
                    new_comb = Comb(pos=(i, j), level=0)
                    self.hive.clist.append(new_comb)
                    print(f"Built new comb at ({i},{j})")
                    return  # Build only one
