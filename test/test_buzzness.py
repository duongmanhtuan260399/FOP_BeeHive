import unittest
from unittest.mock import patch

from model.buzzness import Bee


class TestBee(unittest.TestCase):

    def setUp(self):
        """Set up a Bee object for testing"""
        self.bee = Bee(ID=1, pos=(10, 10))

    def test_initialization(self):
        """Test that a Bee initializes correctly"""
        self.assertEqual(self.bee.ID, 1)
        self.assertEqual(self.bee.pos, (10, 10))
        self.assertEqual(self.bee.age, 0)
        self.assertTrue(self.bee.inhive)
        self.assertFalse(self.bee.hasNectar)

    def test_getters_setters(self):
        """Test getter and setter methods"""
        self.assertEqual(self.bee.get_pos(), (10, 10))
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
        mock_random_choice.return_value = (1, 0)
        old_pos = self.bee.get_pos()

        self.bee.step_change()

        new_pos = self.bee.get_pos()
        expected_pos = (old_pos[0] + 1, old_pos[1] + 0)
        self.assertEqual(new_pos, expected_pos)

if __name__ == '__main__':
    unittest.main()
