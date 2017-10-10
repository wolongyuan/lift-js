from context import lift
from context import tube

from lift import Parser
from lift.Generator import Generator
from lift import Optimizer
from tube import Machine
from tube import Processor

import sys
import StringIO


def test_read(capsys):
    with open('demo/read.js', 'r') as f:
        mock_stdin = StringIO.StringIO("5\nstring\n")
        sys.stdin = mock_stdin

        reload(Parser)
        reload(Generator)
        reload(Machine)
        reload(Processor)
        Parser.build('Program')
        ast = Parser.parse(f.read())
        ast = Optimizer.optimize(ast)
        code = Generator.generate(ast)
        Machine.load(code.splitlines(True))
        Machine.run()
        out, err = capsys.readouterr()
        assert out == "Please enter an integer.\n5\nPlease enter an string.\n'string'\n"

        sys.stdin = sys.__stdin__
