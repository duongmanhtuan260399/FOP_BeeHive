# Bee Simulation Project

## Overview
The Bee Simulation Project is a Python-based simulation that models and visualises bee foraging behaviour. It provides insights into collective intelligence and resource management through a modular design using the Model-View-Controller (MVC) pattern.

## Files Description
- **controller/world_controller.py**: Manages the world interactions, including obstacle detection and bee movement.
- **controller/hive_controller.py**: Handles hive operations, such as nectar storage and path information sharing.
- **model/bee.py**: Defines the Bee class, including movement, energy management, and interaction with the environment.
- **model/hive.py**: Represents the hive structure and manages bee interactions within the hive.
- **model/world.py**: Represents the world grid and properties.
- **view/hive_view.py**: Visualises the hive.
- **view/world_view.py**: Visualises the world.

## Dependencies

- **matplotlib**: Used for visualisation 
- **numpy**: Used for array operations 
- **random**: Used for simulating real-world probabilities 
- **abc**: Used for defining abstract base classes 
- **enum**: Used for defining constants like bee states and property types 
- **unittest**: Used for running unit tests 
- **argparse**: Used for parsing command-line arguments 
- **json** – Used for loading and parsing configuration files.


## How to Run the Program

1. **Install Dependencies**: Example:
   ```bash
   pip install matplotlib numpy
   ```

2. **Run the Tests**: Example:
   ```bash
   python run_tests.py
   ```

3. **Run the Simulation**:
   The program can be run under two modes:
   - **Interactive Mode**: To run the simulation in interactive mode, you can use the following command:
     ```bash
     python main.py -i
     ```
   - **Batch Mode**: To run the simulation in batch mode, you can use the following command:
     ```bash
     python main.py -b
     ```

4. **Command-Line Arguments**:
   Besides the default option, you can modify or create your own parameter.json file and properties.json using command line arguments
   - `-f <properties file location>`: Specifies the location of the properties file containing information of real-world terrains
   - `-p <parameters file location>`: Specifies the location of the parameters file defining the required configurations.