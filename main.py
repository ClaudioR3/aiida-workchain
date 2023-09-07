from aiida import load_profile
load_profile()

import argparse, sys
from aiida.engine import run, submit
from aiida.orm import SinglefileData, Bool
import os
from workchain import PwWorkChain

parser = argparse.ArgumentParser(description='AI4MAT - AiiDA Workflow')
parser.add_argument('-cp', '--calculation-params', default='./params.json', type=str, help='Path of the calculation parameters')
parser.add_argument('-mp', '--mongodb-properties', default='./mongodb.properties', type=str, help='Path of the MongoDB properties')
parser.add_argument('-xyz', '--coordinates', default='./xyz/NaMnO2-angstrom-96.xyz', type=str, help='Path of the material coordinates')
parser.add_argument('--default_generator', action='store_true', help='If true the structure generator function returns the same input structure otherwise the random structure')

args = parser.parse_args(sys.argv[1:])

def main():
    global args
    inputs = {
        'calc_properties': SinglefileData(os.path.abspath(args.calculation_params)),
        'conn_properties': SinglefileData(os.path.abspath(args.mongodb_properties)),
        'xyz_file': SinglefileData(os.path.abspath(args.coordinates)),
        'random_generator': Bool(not args.default_generator)
    }
    run(PwWorkChain, **inputs)

if __name__== "__main__":
    main()
