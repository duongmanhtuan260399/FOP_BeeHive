import unittest
from unittest.mock import Mock, patch
from controller.world_controller import WorldController
from model.world import World, PropertyType, Property
from model.buzzness import Bee, BeeState

class TestWorldController(unittest.TestCase):
    """
    [2.1 World Controller] Test suite for the WorldController class.
    
    This test suite verifies:
    - Controller initialization and basic properties
    - Collision detection between bees and properties
    - Nectar collection from flowers
    - Boundary management and obstacle handling
    """

    def setUp(self):
        """Initialize test environment with common test data"""
        # [2.1 World Controller] Basic setup
        self.hive_pos = (15, 15, 4, 4)
        self.world_size = (50, 50)
        self.world = World(self.hive_pos, self.world_size)
        self.controller = WorldController(self.world, self.world_size)
        
        # Create test properties
        self.properties = {
            'flower': Property(PropertyType.FLOWER, (10, 10), 2, 2, True),
            'tree': Property(PropertyType.TREE, (20, 20), 2, 2, False),
            'water': Property(PropertyType.WATER, (30, 30), 2, 2, False)
        }
        
        # Add properties to world
        for prop in self.properties.values():
            self.world.add_property(prop)

    def _create_test_bee(self, pos=(0, 0), has_nectar=False, in_hive=False):
        """Helper method to create a test bee with specified properties"""
        bee = Bee(1, pos, self.hive_pos, (40, 40), self.world_size)
        bee.hasNectar = has_nectar
        bee.inhive = in_hive
        return bee

    def _mock_bee_methods(self, bee, methods_to_mock=None):
        """Helper method to mock bee methods"""
        if methods_to_mock is None:
            methods_to_mock = ['set_nectar_found', 'step_back']
        
        for method in methods_to_mock:
            setattr(bee, method, Mock())

    def _verify_bee_method_called(self, bee, method_name, called=True, times=1):
        """Helper method to verify bee method calls"""
        method = getattr(bee, method_name)
        if called:
            self.assertEqual(method.call_count, times)
        else:
            self.assertEqual(method.call_count, 0)

    def test_initialization(self):
        """[2.1 World Controller] Test controller initialization"""
        self.assertEqual(self.controller.world, self.world)
        self.assertEqual(self.controller.width, self.world_size[0])
        self.assertEqual(self.controller.height, self.world_size[1])

    def test_check_property_collision(self):
        """[2.1.1 Collision detection] Test property collision detection"""
        # Test collision with property
        bee_pos = (10, 10)  # Inside flower
        self.assertTrue(self.controller._check_property_collision(bee_pos, self.properties['flower']))
        
        # Test no collision
        bee_pos = (5, 5)  # Outside all properties
        self.assertFalse(self.controller._check_property_collision(bee_pos, self.properties['flower']))
        
        # Test edge cases
        bee_pos = (11, 11)  # At property edge
        self.assertTrue(self.controller._check_property_collision(bee_pos, self.properties['flower']))
        
        bee_pos = (12, 12)  # Just outside property
        self.assertFalse(self.controller._check_property_collision(bee_pos, self.properties['flower']))

    def test_handle_flower_interaction(self):
        """[2.1.2 Nectar collection] Test flower interaction handling"""
        bee = self._create_test_bee()
        self._mock_bee_methods(bee)
        
        # Test interaction with flower containing nectar
        self.controller._handle_flower_interaction(bee, self.properties['flower'])
        self.assertFalse(self.properties['flower'].has_nectar)
        self._verify_bee_method_called(bee, 'set_nectar_found')
        
        # Reset the mock before the next call
        bee.set_nectar_found.reset_mock()
        # Test interaction with empty flower
        self.controller._handle_flower_interaction(bee, self.properties['flower'])
        self._verify_bee_method_called(bee, 'set_nectar_found', called=False)

    def test_handle_obstacle_interaction(self):
        """[2.1.1 Collision detection] Test obstacle interaction handling"""
        bee = self._create_test_bee()
        self._mock_bee_methods(bee)
        
        # Test interaction with tree
        self.controller._handle_obstacle_interaction(bee, self.properties['tree'])
        self._verify_bee_method_called(bee, 'step_back', times=1)
        
        # Reset the mock before the next call
        bee.step_back.reset_mock()
        # Test interaction with water
        self.controller._handle_obstacle_interaction(bee, self.properties['water'])
        self._verify_bee_method_called(bee, 'step_back', times=2)

    def test_update_bee_moved_to_flower(self):
        """[2.1.2 Nectar collection] Test bee movement to flower with nectar"""
        bee = self._create_test_bee(pos=(10, 10))
        self._mock_bee_methods(bee)
        
        self.controller._WorldController__update_bee_moved(bee)
        
        self.assertFalse(self.properties['flower'].has_nectar)
        self._verify_bee_method_called(bee, 'set_nectar_found')

    def test_update_bee_moved_to_empty_flower(self):
        """[2.1.2 Nectar collection] Test bee movement to flower without nectar"""
        bee = self._create_test_bee(pos=(10, 10))
        self._mock_bee_methods(bee)
        
        self.properties['flower'].has_nectar = False
        self.controller._WorldController__update_bee_moved(bee)
        
        self._verify_bee_method_called(bee, 'set_nectar_found', called=False)

    def test_update_bee_moved_to_tree(self):
        """[2.1.1 Collision detection] Test bee movement to tree"""
        bee = self._create_test_bee(pos=(20, 20))
        self._mock_bee_methods(bee)
        
        self.controller._WorldController__update_bee_moved(bee)
        
        self._verify_bee_method_called(bee, 'set_nectar_found', called=False)
        self._verify_bee_method_called(bee, 'step_back', times=1)

    def test_update_bee_moved_to_water(self):
        """[2.1.1 Collision detection] Test bee movement to water"""
        bee = self._create_test_bee(pos=(30, 30))
        self._mock_bee_methods(bee)
        
        self.controller._WorldController__update_bee_moved(bee)
        
        self._verify_bee_method_called(bee, 'set_nectar_found', called=False)
        self._verify_bee_method_called(bee, 'step_back', times=2)

    def test_update_bee_in_hive(self):
        """[2.1 World Controller] Test update when bee is in hive"""
        bee = self._create_test_bee(in_hive=True)
        self.controller._WorldController__update_bee_moved = Mock()
        
        self.controller.update(bee)
        
        self.controller._WorldController__update_bee_moved.assert_not_called()

    def test_update_bee_outside_hive(self):
        """[2.1 World Controller] Test update when bee is outside hive"""
        bee = self._create_test_bee(pos=(10, 10))
        self.controller._WorldController__update_bee_moved = Mock()
        
        self.controller.update(bee)
        
        self.controller._WorldController__update_bee_moved.assert_called_once_with(bee)

    def test_update_bee_with_nectar(self):
        """[2.1.2 Nectar collection] Test update when bee already has nectar"""
        bee = self._create_test_bee(pos=(10, 10), has_nectar=True)
        self._mock_bee_methods(bee)
        
        self.controller._WorldController__update_bee_moved(bee)
        
        self._verify_bee_method_called(bee, 'set_nectar_found', called=False)
        self._verify_bee_method_called(bee, 'step_back', called=False)

    def test_obstacle_detection(self):
        """[2.1.1 Collision detection] Test obstacle detection and bee movement prevention"""
        bee = self._create_test_bee(pos=(20, 20))
        self._mock_bee_methods(bee)
        
        self.controller._WorldController__update_bee_moved(bee)
        
        self._verify_bee_method_called(bee, 'step_back', times=1)

    def test_multiple_obstacles(self):
        """[2.1.1 Collision detection] Test handling of multiple obstacles"""
        # Add another obstacle near the first one
        self.world.add_property(Property(PropertyType.TREE, (21, 21), 2, 2, False))
        
        bee = self._create_test_bee(pos=(20, 20))
        self._mock_bee_methods(bee)
        
        self.controller._WorldController__update_bee_moved(bee)
        
        self._verify_bee_method_called(bee, 'step_back', times=1)

    def test_obstacle_edge_cases(self):
        """[2.1.1 Collision detection] Test obstacle detection at property edges"""
        # Test bee at property edge
        bee = self._create_test_bee(pos=(19, 20))
        self._mock_bee_methods(bee)
        
        self.controller._WorldController__update_bee_moved(bee)
        self._verify_bee_method_called(bee, 'step_back', called=False)
        
        # Test bee at property corner
        bee.pos = (20, 20)
        self.controller._WorldController__update_bee_moved(bee)
        self._verify_bee_method_called(bee, 'step_back', times=1)

if __name__ == '__main__':
    unittest.main() 