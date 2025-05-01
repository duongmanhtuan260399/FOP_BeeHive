import argparse
import json
from view.MainView import MainView

# Read args
parser = argparse.ArgumentParser(description='Simulate bee foraging and comb building.')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-i','--interactive',action='store_true',help='Interactive mode')
group.add_argument('-b','--batch',action='store_true',help='Batch mode')
parser.add_argument('-f','--map_file',type=str,help='Config JSON for world')
parser.add_argument('-p','--param_file',type=str,help='Params JSON')
parser.add_argument('--visualize',action='store_true',help='Enable visualization')
args = parser.parse_args()

# Setup view
mainView = MainView()

if args.interactive:
    ts=int(input('Timesteps: ')); nb=int(input('Bees: ')); cf=input('Config file: ')
    mainView.simulate(ts, nb, cf, visualize=args.visualize)
else:
    if not args.map_file or not args.param_file:
        parser.error('Batch needs --map_file and --param_file')
    params=json.load(open(args.param_file))
    mainView.simulate(params.get('time_steps',100), params.get('num_bees',5), args.map_file, visualize=args.visualize)
