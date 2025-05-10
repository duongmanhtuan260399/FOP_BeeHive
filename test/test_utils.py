import unittest
from utils.utils import find_path_to_flower, find_path_to_hive
from utils.constants import VALID_MOVE


class TestUtils(unittest.TestCase):
    def setUp(self):
        """Set up test cases with common positions"""
        self.hive_pos = (15, 15)
        self.flower_pos = (20, 20)
        self.current_pos = (10, 10)

    def test_find_path_to_flower_same_position(self):
        """Test path finding when start and end positions are the same"""
        path = find_path_to_flower(self.hive_pos, self.hive_pos)
        self.assertEqual(path, [], "Path should be empty when start and end positions are the same")

    def test_find_path_to_flower_diagonal(self):
        """Test path finding for diagonal movement"""
        path = find_path_to_flower(self.hive_pos, self.flower_pos)
        
        # Verify path properties
        self.assertGreater(len(path), 0, "Path should not be empty")
        self.assertTrue(all(move in VALID_MOVE for move in path), "All moves should be valid")
        
        # Verify path leads to target
        current = list(self.hive_pos)
        for move in path:
            current[0] += move[0]
            current[1] += move[1]
        self.assertEqual(tuple(current), self.flower_pos, "Path should lead to target position")

    def test_find_path_to_flower_horizontal(self):
        """Test path finding for horizontal movement"""
        target_pos = (self.hive_pos[0] + 5, self.hive_pos[1])
        path = find_path_to_flower(self.hive_pos, target_pos)
        
        # Verify path properties
        self.assertGreater(len(path), 0, "Path should not be empty")
        self.assertTrue(all(move in VALID_MOVE for move in path), "All moves should be valid")
        
        # Verify path leads to target
        current = list(self.hive_pos)
        for move in path:
            current[0] += move[0]
            current[1] += move[1]
        self.assertEqual(tuple(current), target_pos, "Path should lead to target position")

    def test_find_path_to_flower_vertical(self):
        """Test path finding for vertical movement"""
        target_pos = (self.hive_pos[0], self.hive_pos[1] + 5)
        path = find_path_to_flower(self.hive_pos, target_pos)
        
        # Verify path properties
        self.assertGreater(len(path), 0, "Path should not be empty")
        self.assertTrue(all(move in VALID_MOVE for move in path), "All moves should be valid")
        
        # Verify path leads to target
        current = list(self.hive_pos)
        for move in path:
            current[0] += move[0]
            current[1] += move[1]
        self.assertEqual(tuple(current), target_pos, "Path should lead to target position")

    def test_find_path_to_flower_negative_direction(self):
        """Test path finding for negative direction movement"""
        target_pos = (self.hive_pos[0] - 5, self.hive_pos[1] - 5)
        path = find_path_to_flower(self.hive_pos, target_pos)
        
        # Verify path properties
        self.assertGreater(len(path), 0, "Path should not be empty")
        self.assertTrue(all(move in VALID_MOVE for move in path), "All moves should be valid")
        
        # Verify path leads to target
        current = list(self.hive_pos)
        for move in path:
            current[0] += move[0]
            current[1] += move[1]
        self.assertEqual(tuple(current), target_pos, "Path should lead to target position")

    def test_find_path_to_hive_same_position(self):
        """Test path finding when start and end positions are the same"""
        path = find_path_to_hive(self.hive_pos, self.hive_pos)
        self.assertEqual(path, [], "Path should be empty when start and end positions are the same")

    def test_find_path_to_hive_diagonal(self):
        """Test path finding for diagonal movement to hive"""
        path = find_path_to_hive(self.hive_pos, self.current_pos)
        
        # Verify path properties
        self.assertGreater(len(path), 0, "Path should not be empty")
        self.assertTrue(all(move in VALID_MOVE for move in path), "All moves should be valid")
        
        # Verify path leads to target
        current = list(self.current_pos)
        for move in path:
            current[0] += move[0]
            current[1] += move[1]
        self.assertEqual(tuple(current), self.hive_pos, "Path should lead to target position")

    def test_find_path_to_hive_horizontal(self):
        """Test path finding for horizontal movement to hive"""
        start_pos = (self.hive_pos[0] + 5, self.hive_pos[1])
        path = find_path_to_hive(self.hive_pos, start_pos)
        
        # Verify path properties
        self.assertGreater(len(path), 0, "Path should not be empty")
        self.assertTrue(all(move in VALID_MOVE for move in path), "All moves should be valid")
        
        # Verify path leads to target
        current = list(start_pos)
        for move in path:
            current[0] += move[0]
            current[1] += move[1]
        self.assertEqual(tuple(current), self.hive_pos, "Path should lead to target position")

    def test_find_path_to_hive_vertical(self):
        """Test path finding for vertical movement to hive"""
        start_pos = (self.hive_pos[0], self.hive_pos[1] + 5)
        path = find_path_to_hive(self.hive_pos, start_pos)
        
        # Verify path properties
        self.assertGreater(len(path), 0, "Path should not be empty")
        self.assertTrue(all(move in VALID_MOVE for move in path), "All moves should be valid")
        
        # Verify path leads to target
        current = list(start_pos)
        for move in path:
            current[0] += move[0]
            current[1] += move[1]
        self.assertEqual(tuple(current), self.hive_pos, "Path should lead to target position")

    def test_find_path_to_hive_negative_direction(self):
        """Test path finding for negative direction movement to hive"""
        start_pos = (self.hive_pos[0] - 5, self.hive_pos[1] - 5)
        path = find_path_to_hive(self.hive_pos, start_pos)
        
        # Verify path properties
        self.assertGreater(len(path), 0, "Path should not be empty")
        self.assertTrue(all(move in VALID_MOVE for move in path), "All moves should be valid")
        
        # Verify path leads to target
        current = list(start_pos)
        for move in path:
            current[0] += move[0]
            current[1] += move[1]
        self.assertEqual(tuple(current), self.hive_pos, "Path should lead to target position")

    def test_find_path_invalid_input(self):
        """Test path finding with invalid input types"""
        with self.assertRaises(TypeError):
            find_path_to_flower("invalid", self.flower_pos)
        
        with self.assertRaises(TypeError):
            find_path_to_hive(self.hive_pos, "invalid")


if __name__ == '__main__':
    unittest.main() 