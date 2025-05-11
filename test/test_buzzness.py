import unittest
from unittest.mock import patch
from model.buzzness import Bee, BeeState
from utils.constants import VALID_MOVE, MOVE_FORWARD


class TestBee(unittest.TestCase):

    def setUp(self):
        self.hive_pos = (15, 15, 4, 4)
        self.hive_size = (40, 40)
        self.world_size = (50, 50)
        self.bee = Bee(1, (0, 0), self.hive_pos, self.hive_size, self.world_size)

    def test_initialization(self):
        """[1.1 Bee] Test bee initialization and basic properties"""
        self.assertEqual(self.bee.ID, 1)
        self.assertEqual(self.bee.pos, (0, 0))
        self.assertTrue(self.bee.inhive)
        self.assertFalse(self.bee.hasNectar)
        self.assertEqual(self.bee.state, BeeState.WANDERING)
        self.assertEqual(self.bee.energy, 0)

    def test_state_transitions(self):
        """[1.1.1 State Management] Test bee state transitions"""
        # Test energy charging in hive
        self.bee.energy = 0
        self.bee.step_change()
        self.assertEqual(self.bee.energy, 25)

        # Test leaving hive when charged
        self.bee.energy = 60
        self.bee.step_change()
        self.assertFalse(self.bee.inhive)

    def test_movement(self):
        """[1.1.2 Movement] Test bee movement mechanics"""
        initial_pos = self.bee.pos

        # Test movement within bounds
        self.bee._execute_move((1, 1))
        self.assertNotEqual(self.bee.pos, initial_pos)

        # Test movement at world boundaries
        self.bee.pos = (self.world_size[0]-3, self.world_size[1]-3)
        self.bee._execute_move((1, 1))
        self.assertEqual(self.bee.pos, (self.world_size[0]-2, self.world_size[1]-2))  # Should stay at safe distance from boundary

    def test_nectar_collection(self):
        """[1.1.4 Path finding] Test bee nectar collection behavior"""
        # Test setting nectar found
        self.bee.set_nectar_found()
        self.assertTrue(self.bee.hasNectar)
        self.assertEqual(self.bee.state, BeeState.RETURNING)
        self.assertFalse(self.bee.inhive)

    def test_energy_management(self):
        """[1.1.3 Energy Management] Test bee energy management"""
        # Test energy decrease during movement
        initial_energy = 50
        self.bee.energy = initial_energy
        self.bee._execute_move((1, 1))
        self.assertEqual(self.bee.energy, initial_energy - 1)

        # Test energy charging in hive
        self.bee.energy = 0
        self.bee.inhive = True
        self.bee.step_change()
        self.assertEqual(self.bee.energy, 25)

    def test_getters_setters(self):
        """[1.1 Bee] Test getter and setter methods"""
        self.assertEqual(self.bee.get_pos(), (0, 0))
        self.assertTrue(self.bee.get_inhive())

        self.bee.set_inhive(False)
        self.assertFalse(self.bee.get_inhive())

        self.assertFalse(self.bee.get_nectar())

        self.bee.set_nectar(True)
        self.assertTrue(self.bee.get_nectar())

    @patch('random.choice')
    def test_step_change(self, mock_random_choice):
        """[1.1 Bee] Test that step_change correctly updates the bee's position"""
        # Mock random.choice to always pick (1, 0)
        self.bee.inhive = False
        self.bee.pos = (20,20)
        self.bee.energy = 50
        mock_random_choice.return_value = (1, 0)
        old_pos = self.bee.get_pos()

        self.bee.step_change()

        new_pos = self.bee.get_pos()
        expected_pos = (old_pos[0] + 1, old_pos[1] + 0)
        self.assertEqual(new_pos, expected_pos)

    def test_movement_with_obstacle(self):
        """[1.1.2 Movement] Test bee movement when encountering an obstacle"""
        # Setup bee outside hive
        self.bee.inhive = False
        self.bee.pos = (10, 10)
        self.bee.energy = 50
        
        # Test WANDERING state
        self.bee.state = BeeState.WANDERING
        initial_pos = self.bee.pos
        
        # Simulate hitting an obstacle
        self.bee._move_invalid = False
        self.bee.step_back()
        
        # Verify the move was marked as invalid
        self.assertTrue(self.bee._move_invalid)
        
        # Try to move
        result = self.bee._execute_move((1, 1))
        
        # For WANDERING state, should try alternative move
        self.assertNotEqual(self.bee.pos, initial_pos)
        self.assertTrue(result)
        
        # Test FOLLOWING state
        self.bee.state = BeeState.FOLLOWING
        self.bee.pos = (10, 10)
        initial_pos = self.bee.pos
        self.bee._move_invalid = False
        self.bee.step_back()
        
        # Try to move
        result = self.bee._execute_move((1, 1))
        
        # For FOLLOWING state, should stay in same position
        self.assertEqual(self.bee.pos, initial_pos)
        self.assertFalse(result)
        
        # Test RETURNING state
        self.bee.state = BeeState.RETURNING
        self.bee.pos = (10, 10)
        initial_pos = self.bee.pos
        self.bee._move_invalid = False
        self.bee.step_back()
        
        # Try to move
        result = self.bee._execute_move((1, 1))
        
        # For RETURNING state, should stay in same position
        self.assertEqual(self.bee.pos, initial_pos)
        self.assertFalse(result)

    def test_boundary_behavior(self):
        """[1.1.2 Movement] Test bee behavior when reaching world boundaries"""
        # Setup bee outside hive
        self.bee.inhive = False
        self.bee.energy = 50
        
        # Test WANDERING state
        self.bee.state = BeeState.WANDERING
        
        # Test right boundary
        self.bee.pos = (self.world_size[0] - 3, 10)
        initial_pos = self.bee.pos
        result = self.bee._execute_move((2, 0))  # Try to move beyond right boundary
        # Should try alternative move and not stay at boundary
        self.assertNotEqual(self.bee.pos, initial_pos)
        self.assertTrue(result)
        
        # Test FOLLOWING state
        self.bee.state = BeeState.FOLLOWING
        self.bee.pos = (self.world_size[0] - 3, 10)
        initial_pos = self.bee.pos
        result = self.bee._execute_move((2, 0))  # Try to move beyond right boundary
        # Should stay at boundary
        self.assertEqual(self.bee.pos, (self.world_size[0] - 2, 10))
        self.assertTrue(result)
        
        # Test RETURNING state
        self.bee.state = BeeState.RETURNING
        self.bee.pos = (self.world_size[0] - 3, 10)
        initial_pos = self.bee.pos
        result = self.bee._execute_move((2, 0))  # Try to move beyond right boundary
        # Should stay at boundary
        self.assertEqual(self.bee.pos, (self.world_size[0] - 2, 10))
        self.assertTrue(result)

    def test_hive_to_world_transition(self):
        """[1.1.1 State Management] Test bee transition from hive to world"""
        # Setup bee in hive with enough energy
        self.bee.inhive = True
        self.bee.energy = 60
        self.bee.pos = (0, 0)
        
        # Test WANDERING state
        self.bee.state = BeeState.WANDERING
        self.bee.step_change()
        self.assertFalse(self.bee.inhive)
        self.assertEqual(self.bee.pos, (self.hive_pos[0], self.hive_pos[1]))
        
        # Reset bee
        self.bee.inhive = True
        self.bee.pos = (0, 0)
        
        # Test FOLLOWING state
        self.bee.state = BeeState.FOLLOWING
        self.bee.path_to_flower = [(1, 1), (2, 2)]  # Add some path
        self.bee.step_change()
        self.assertFalse(self.bee.inhive)
        self.assertEqual(self.bee.pos, (self.hive_pos[0], self.hive_pos[1]))
        
        # Reset bee
        self.bee.inhive = True
        self.bee.pos = (0, 0)
        
        # Test RETURNING state (should not leave hive)
        self.bee.state = BeeState.RETURNING
        self.bee.step_change()
        self.assertTrue(self.bee.inhive)
        self.assertEqual(self.bee.pos, (0, 0))


if __name__ == '__main__':
    unittest.main()
