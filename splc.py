import argparse
import os

from compiler.main import Compiler

version = '1.0'

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--target', default=['x64'], type=str, nargs=1, choices=['x64', 'ssm'],
                    help='Target platform to compile to')
parser.add_argument('-i', '--input', required=True, type=str, nargs=1, help='SPL input file to compile')
parser.add_argument('-o', '--output', type=str, nargs=1, help='Output file', default=[f'{os.getcwd()}/out'])
parser.add_argument('-v', '--verbosity', type=str, nargs=1, help='Verbosity level', default=['info'],
                    choices=['debug', 'info', 'warning', 'error'])


args = parser.parse_args()

compiler = Compiler(args.verbosity[0])
print(f'Starting SPL compiler version {version}')
compiler.compile(args.input[0], args.target[0], args.output[0])
