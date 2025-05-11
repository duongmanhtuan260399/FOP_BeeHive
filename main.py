import argparse
import json
import sys
from json import JSONDecodeError

import utils.constants
from view.MainView import MainView

# Read args
parser = argparse.ArgumentParser(description='Simulate bee foraging and comb building.')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-i','--interactive',action='store_true',help='Interactive mode')
group.add_argument('-b','--batch',action='store_true',help='Batch mode')
parser.add_argument('-f','--map_file',type=str,help='Config JSON for world')
parser.add_argument('-p','--param_file',type=str,help='Params JSON')
args = parser.parse_args()

# Setup view
mainView = MainView()

def _value_in_range(value, minimum, maximum):
    if value < minimum or value > maximum:
        return False
    return True

def get_positive_int(prompt, minimum, maximum):
    while True:
        try:
            value = int(input(prompt))
            if not _value_in_range(value, minimum, maximum):
                print(f"Invalid input. Please enter a positive value between {minimum} and {maximum}.")
            else:
                return value
        except ValueError:
            print('Invalid input. Please enter a positive number')

param_file = args.param_file if args.param_file else utils.constants.PARAMETER_FILE
map_file = args.map_file if args.map_file else utils.constants.PROPERTY_FILE

if args.interactive:
    ts = get_positive_int('Timesteps: ', 1, 10000)
    nb = get_positive_int('Bees: ',1,100)
    mainView.simulate(ts, nb, map_file)
else:
    try:
        with open(param_file) as f:
            params = json.load(f)
    except FileNotFoundError:
        print(f'Error: Parameter file {param_file} not found.')
        sys.exit(1)
    except JSONDecodeError:
        print(f'Error: Parameter file {param_file} is not a valid JSON file.')
        sys.exit(1)
    try:
        ts = int(params.get('time_steps'))
        nb = int(params.get('num_bees'))
    except (KeyError, ValueError, TypeError):
        print(f'Error: Invalid parameters in {param_file}')
        sys.exit(1)
    if not _value_in_range(ts, 1, 10000):
        print(f"Invalid input. Please enter number of time steps between 1 and 10000.")
        sys.exit(1)
    if not _value_in_range(nb, 1, 100):
        print(f"Invalid input. Please enter number of bees between 1 and 100.")
        sys.exit(1)
    mainView.simulate(ts, nb, map_file)
