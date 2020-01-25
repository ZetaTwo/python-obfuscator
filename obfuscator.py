#!/usr/bin/env python3

import argparse
import ast
import sys
import importlib._bootstrap_external
import importlib.util


parser = argparse.ArgumentParser(description='Obfuscate Python bytecode')
parser.add_argument('filename', type=str, help='The code to obfuscate')
parser.add_argument('outfile', type=str, nargs='?', default=None, help='The destination file for the obfuscated bytecode')
args = parser.parse_args()

infile, outfile = args.filename, args.outfile
if outfile is None:
    infile_tokens = infile.split('.')
    if infile_tokens[-1] == 'py':
        infile_tokens[-1] = 'obf'
    else:
        infile_tokens.append('obf')    
    infile_tokens.append('pyc')
    outfile = '.'.join(infile_tokens)

try:
    with open(args.filename, 'r') as fin:
        sourcecode = fin.read()
        tree = ast.parse(sourcecode, filename=args.filename)
except IOError as e:
    print(f'Failed to open {args.filename}: {e}')
    sys.exit(1)
except Exception as e:
    print(f'Error: {e}')
    sys.exit(1)

class RewriteName(ast.NodeTransformer):
    def __init__(self):
        self.stored_vars = {}

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.stored_vars[node.id] = len(self.stored_vars)
        
        if node.id.startswith('EVIL'):
            #node.id = "y = 'Hello' #"
            node.id = "i = 0\n    j"

        """
        var_num = self.stored_vars.get(node.id, None)
        if var_num is not None:
            node.id = 'MOD_' + node.id
            #node.id = ' '*(var_num+1)
        """

        return node

 

rewriter = RewriteName()
tree = rewriter.visit(tree)

ast.fix_missing_locations(tree)
code = compile(tree, args.filename, 'exec')

# Create the .pyc file
# Based on https://github.com/python/cpython/blob/3.8/Lib/py_compile.py
loader = importlib.machinery.SourceFileLoader('<py_compile>', args.filename)
source_stats = loader.path_stats(args.filename)
bytecode = importlib._bootstrap_external._code_to_timestamp_pyc(code, 
    source_stats['mtime'], source_stats['size'])
mode = importlib._bootstrap_external._calc_mode(args.filename)
importlib._bootstrap_external._write_atomic(outfile, bytecode, mode) 
