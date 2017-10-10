#!env/bin/python
"""Lift JS

Usage:
    main.py <file>  [-o <file>]

Options:
    -o <file>, --output <file>      Specifies output file [default: a.out].

"""
import Parser
import Optimizer
import sys
from Generator import Generator
from docopt import docopt

if __name__ == '__main__':
    args = docopt(__doc__)
    input_file = args['<file>']
    output_file = args['--output']
    ast = None
    try:
        with open(input_file, 'r') as f:
            Parser.build("Program")
            source = f.read()
            ast = Parser.parse(source)
    except IOError:
        print('Error opening file %s. Please check the file or '
              'the directory.' % input_file)
        sys.exit(1)

    if ast is None:
        error_list = list(Parser.error_list.keys())
        error_list.sort()
        for key in error_list:
            sys.stdout.write(Parser.error_list[key])
        sys.stdout.flush()
        sys.exit(-1)

    ast = Optimizer.optimize(ast)

    try:
        with open(output_file, 'w') as f:
            f.write(Generator.generate(ast))
    except IOError:
        print('Error writing to file %s. Please check the file or '
              'the directory.' % output_file)
        sys.exit(1)
