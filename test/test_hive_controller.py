import unittest
from unittest.mock import Mock, patch
from controller.hive_controller import HiveController
from model.hive import Hive, Comb
from model.buzzness import Bee

class TestHiveController(unittest.TestCase):
    """
    [2.2 Hive Controller] Test suite for the HiveController class.
    
    This test suite verifies:
    - Controller initialization and basic properties
    - Nectar storage in hive combs
    - Path information sharing between bees
    - Bee state management when returning to hive
    """

    def setUp(self):
        """Initialize test environment with common test data"""
        # [2.2 Hive Controller] Basic setup
        self.hive = Hive((40, 40))
        self.controller = HiveController(self.hive)
        
        # Create a test bee
        self.bee = Bee(1, (0, 0), (15, 15, 4, 4), (40, 40), (50, 50))

        # Create some test combs
        self.comb1 = Comb((1, 1))
        self.comb2 = Comb((2, 2))
        self.hive.clist = [self.comb1, self.comb2]

    def test_initialization(self):
        """[2.2 Hive Controller] Test controller initialization"""
        self.assertEqual(self.controller.hive, self.hive)
        self.assertEqual(self.controller.path_to_flower, [])

    def test_add_nectar(self):
        """[2.2.1 Nectar storage] Test adding nectar to combs"""
        # Test adding nectar to empty comb
        self.controller._HiveController__add_nectar()
        self.assertTrue(self.comb1.has_nectar)
        
        # Test adding nectar to second comb when first is full
        self.controller._HiveController__add_nectar()
        self.assertTrue(self.comb2.has_nectar)

    def test_spread_path(self):
        """[2.2.2 Path information sharing] Test spreading path information"""
        test_path = [(1, 1), (2, 2), (3, 3)]
        self.controller._HiveController__spread_path(test_path)
        self.assertEqual(self.controller.path_to_flower, test_path)

    def test_update_with_nectar(self):
        """[2.2 Hive Controller] Test update when bee returns with nectar"""
        # Setup bee with nectar and path
        self.bee.hasNectar = True
        self.bee.inhive = True
        self.bee.path_to_flower = [(1, 1), (2, 2)]
        
        # Mock notify method
        self.controller.notify = Mock()
        
        # Test update
        self.controller.update(self.bee)
        
        # Verify bee's nectar was removed
        self.assertFalse(self.bee.hasNectar)
        # Verify path was spread
        self.assertEqual(self.controller.path_to_flower, [(1, 1), (2, 2)])
        # Verify notify was called
        self.controller.notify.assert_called_once()

    def test_update_without_nectar(self):
        """[2.2 Hive Controller] Test update when bee returns without nectar"""
        # Setup bee without nectar
        self.bee.hasNectar = False
        self.bee.inhive = True
        
        # Mock notify method
        self.controller.notify = Mock()
        
        # Test update
        self.controller.update(self.bee)
        
        # Verify notify was not called
        self.controller.notify.assert_not_called()

    def test_update_when_not_in_hive(self):
        """[2.2 Hive Controller] Test update when bee is not in hive"""
        # Setup bee not in hive
        self.bee.inhive = False
        self.bee.hasNectar = True
        
        # Mock notify method
        self.controller.notify = Mock()
        
        # Test update
        self.controller.update(self.bee)
        
        # Verify notify was not called
        self.controller.notify.assert_not_called()

if __name__ == '__main__':
    unittest.main() 