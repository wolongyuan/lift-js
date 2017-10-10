#!env/bin/python
"""Tube VM

Usage:
    main.py <file> 

"""
from docopt import docopt
import sys
import Machine


if __name__ == '__main__':
    args = docopt(__doc__)
    input_file = args['<file>']
    try:
        with open(input_file, 'r') as f:
            Machine.load(f.readlines())
            Machine.run()
    except IOError:
        print 'Error opening file %s. Please check the file or ' \
              'the directory.' % input_file
        sys.exit(1)

