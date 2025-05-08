import unittest
from unittest.mock import patch
from model.buzzness import Bee, BeeState


class TestBee(unittest.TestCase):

    def setUp(self):
        self.hive_pos = (15, 15, 4, 4)
        self.hive_size = (40, 40)
        self.world_size = (50, 50)
        self.bee = Bee(1, (0, 0), self.hive_pos, self.hive_size, self.world_size)

    def test_initialization(self):
        """Test bee initialization and basic properties"""
        self.assertEqual(self.bee.ID, 1)
        self.assertEqual(self.bee.pos, (0, 0))
        self.assertTrue(self.bee.inhive)
        self.assertFalse(self.bee.hasNectar)
        self.assertEqual(self.bee.state, BeeState.WANDERING)
        self.assertEqual(self.bee.energy, 0)

    def test_state_transitions(self):
        """Test bee state transitions"""
        # Test energy charging in hive
        self.bee.energy = 0
        self.bee.step_change()
        self.assertEqual(self.bee.energy, 25)

        # Test leaving hive when charged
        self.bee.energy = 60
        self.bee.step_change()
        self.assertFalse(self.bee.inhive)

    def test_movement(self):
        """Test bee movement mechanics"""
        initial_pos = self.bee.pos

        # Test movement within bounds
        self.bee._Bee__move((1, 1))
        self.assertNotEqual(self.bee.pos, initial_pos)

        # Test movement at world boundaries
        self.bee.pos = (self.world_size[0]-1, self.world_size[1]-1)
        self.bee._Bee__move((1, 1))
        self.assertEqual(self.bee.pos, (self.world_size[0]-1, self.world_size[1]-1))

    def test_nectar_collection(self):
        """Test bee nectar collection behavior"""
        # Test setting nectar found
        self.bee.set_nectar_found()
        self.assertTrue(self.bee.hasNectar)
        self.assertEqual(self.bee.state, BeeState.RETURNING)
        self.assertFalse(self.bee.inhive)

    def test_energy_management(self):
        """Test bee energy management"""
        # Test energy decrease during movement
        initial_energy = 50
        self.bee.energy = initial_energy
        self.bee._Bee__move((1, 1))
        self.assertEqual(self.bee.energy, initial_energy - 1)

        # Test energy charging in hive
        self.bee.energy = 0
        self.bee.inhive = True
        self.bee.step_change()
        self.assertEqual(self.bee.energy, 25)

    def test_getters_setters(self):
        """Test getter and setter methods"""
        self.assertEqual(self.bee.get_pos(), (0, 0))
        self.assertTrue(self.bee.get_inhive())

        self.bee.set_inhive(False)
        self.assertFalse(self.bee.get_inhive())

        self.assertFalse(self.bee.get_nectar())

        self.bee.set_nectar(True)
        self.assertTrue(self.bee.get_nectar())

    @patch('random.choice')
    def test_step_change(self, mock_random_choice):
        """Test that step_change correctly updates the bee's position"""
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

if __name__ == '__main__':
    unittest.main()
