import unittest
from utils.utils import find_path_to_flower, find_path_to_hive

class TestUtils(unittest.TestCase):
    def test_find_path_to_flower_same_position(self):
        """Test pathfinding when start and end positions are the same"""
        hive_pos = (10, 10)
        flower_pos = (10, 10)
        
        path = find_path_to_flower(hive_pos, flower_pos)
        self.assertEqual(path, [])

    def test_find_path_to_flower_horizontal(self):
        """Test pathfinding for horizontal movement"""
        hive_pos = (10, 10)
        flower_pos = (15, 10)  # 5 steps to the right
        
        path = find_path_to_flower(hive_pos, flower_pos)
        self.assertEqual(len(path), 5)
        self.assertTrue(all(move == (1, 0) for move in path))

    def test_find_path_to_flower_vertical(self):
        """Test pathfinding for vertical movement"""
        hive_pos = (10, 10)
        flower_pos = (10, 15)  # 5 steps up
        
        path = find_path_to_flower(hive_pos, flower_pos)
        self.assertEqual(len(path), 5)
        self.assertTrue(all(move == (0, 1) for move in path))

    def test_find_path_to_flower_diagonal(self):
        """Test pathfinding for diagonal movement"""
        hive_pos = (10, 10)
        flower_pos = (15, 15)  # 5 steps diagonally
        
        path = find_path_to_flower(hive_pos, flower_pos)
        self.assertEqual(len(path), 5)
        self.assertTrue(all(move == (1, 1) for move in path))

    def test_find_path_to_flower_negative_direction(self):
        """Test pathfinding in negative directions"""
        hive_pos = (15, 15)
        flower_pos = (10, 10)  # 5 steps diagonally in negative direction
        
        path = find_path_to_flower(hive_pos, flower_pos)
        self.assertEqual(len(path), 5)
        self.assertTrue(all(move == (-1, -1) for move in path))

    def test_find_path_to_hive_same_position(self):
        """Test pathfinding to hive when already at hive"""
        hive_pos = (10, 10)
        current_pos = (10, 10)
        
        path = find_path_to_hive(hive_pos, current_pos)
        self.assertEqual(path, [])

    def test_find_path_to_hive_horizontal(self):
        """Test pathfinding to hive for horizontal movement"""
        hive_pos = (10, 10)
        current_pos = (15, 10)  # 5 steps to the right of hive
        
        path = find_path_to_hive(hive_pos, current_pos)
        self.assertEqual(len(path), 5)
        self.assertTrue(all(move == (-1, 0) for move in path))

    def test_find_path_to_hive_vertical(self):
        """Test pathfinding to hive for vertical movement"""
        hive_pos = (10, 10)
        current_pos = (10, 15)  # 5 steps up from hive
        
        path = find_path_to_hive(hive_pos, current_pos)
        self.assertEqual(len(path), 5)
        self.assertTrue(all(move == (0, -1) for move in path))

    def test_find_path_to_hive_diagonal(self):
        """Test pathfinding to hive for diagonal movement"""
        hive_pos = (10, 10)
        current_pos = (15, 15)  # 5 steps diagonally from hive
        
        path = find_path_to_hive(hive_pos, current_pos)
        self.assertEqual(len(path), 5)
        self.assertTrue(all(move == (-1, -1) for move in path))

    def test_find_path_to_hive_negative_direction(self):
        """Test pathfinding to hive in negative directions"""
        hive_pos = (15, 15)
        current_pos = (10, 10)  # 5 steps diagonally in negative direction from hive
        
        path = find_path_to_hive(hive_pos, current_pos)
        self.assertEqual(len(path), 5)
        self.assertTrue(all(move == (1, 1) for move in path))

    def test_pathfinding_max_iterations(self):
        """Test pathfinding with maximum iterations"""
        hive_pos = (0, 0)
        flower_pos = (10001, 10001)  # Very far position
        
        with self.assertRaises(RuntimeError) as context:
            find_path_to_flower(hive_pos, flower_pos)
        self.assertTrue("Pathfinding exceeded maximum iterations" in str(context.exception))

    def test_pathfinding_consistency(self):
        """Test that pathfinding is consistent in both directions"""
        hive_pos = (10, 10)
        flower_pos = (15, 15)
        
        # Path from hive to flower
        path_to_flower = find_path_to_flower(hive_pos, flower_pos)
        
        # Path from flower to hive
        path_to_hive = find_path_to_hive(hive_pos, flower_pos)
        
        # The paths should be the same length
        self.assertEqual(len(path_to_flower), len(path_to_hive))
        
        # The moves should be opposite of each other
        for to_flower, to_hive in zip(path_to_flower, path_to_hive):
            self.assertEqual(to_flower[0], -to_hive[0])
            self.assertEqual(to_flower[1], -to_hive[1])

if __name__ == '__main__':
    unittest.main() 