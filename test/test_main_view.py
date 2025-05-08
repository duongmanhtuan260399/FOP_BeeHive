import unittest
import json
import tempfile
from unittest.mock import patch, MagicMock
from view.MainView import MainView
from model.world import World, PropertyType

class TestMainView(unittest.TestCase):
    def setUp(self):
        self.main_view = MainView()
        self.hive_pos = (15, 15, 4, 4)
        self.world_size = (50, 50)
        
        # Create a temporary config file for testing
        self.temp_config = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.config_data = {
            "properties": {
                "trees": [{"x": 10, "y": 10, "width": 2, "height": 2}],
                "flower": [{"x": 20, "y": 20, "width": 1, "height": 1}],
                "water": [{"x": 30, "y": 30, "width": 3, "height": 3}]
            }
        }
        json.dump(self.config_data, self.temp_config)
        self.temp_config.close()

    def tearDown(self):
        import os
        os.unlink(self.temp_config.name)

    def test_property_reading(self):
        """Test reading properties from config file"""
        world = World(self.hive_pos, self.world_size)
        self.main_view.read_property(self.temp_config.name, world)
        
        properties = world.properties
        self.assertTrue(any(p.type == PropertyType.TREE for p in properties))
        self.assertTrue(any(p.type == PropertyType.FLOWER for p in properties))
        self.assertTrue(any(p.type == PropertyType.WATER for p in properties))

    @patch('matplotlib.pyplot.show')
    def test_simulation_visualization(self, mock_show):
        """Test simulation with visualization"""
        history = self.main_view.simulate(
            time_steps=2,
            num_bees=2,
            config_file=self.temp_config.name,
            visualize=True
        )
        self.assertIsNotNone(history)

    def test_simulation_without_visualization(self):
        """Test simulation without visualization"""
        history = self.main_view.simulate(
            time_steps=2,
            num_bees=2,
            config_file=self.temp_config.name,
            visualize=False
        )
        self.assertIsNotNone(history)

    def test_invalid_config_file(self):
        """Test handling of invalid config file"""
        world = World(self.hive_pos, self.world_size)
        with self.assertRaises(Exception):
            self.main_view.read_property("nonexistent_file.json", world)

    def test_simulation_parameters(self):
        """Test simulation with different parameters"""
        # Test with different number of bees
        history = self.main_view.simulate(
            time_steps=2,
            num_bees=5,  # More bees
            config_file=self.temp_config.name,
            visualize=False
        )
        self.assertIsNotNone(history)

        # Test with different time steps
        history = self.main_view.simulate(
            time_steps=5,  # More time steps
            num_bees=2,
            config_file=self.temp_config.name,
            visualize=False
        )
        self.assertIsNotNone(history)

if __name__ == '__main__':
    unittest.main() 