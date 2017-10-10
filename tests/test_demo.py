from context import lift
from context import tube

from lift import Parser
from lift.Generator import Generator
from lift import Optimizer
from tube import Machine
from tube import Processor

import pytest


@pytest.mark.parametrize("source, result", [
    ('demo/var.js', "'This is a string.'\n5\n"),
    ('demo/show.js', "1\n'Hello everybody!'\n{'key1': 'val1', 'key2': 'val2'}\n'Built-in function panel.show().'\n"),
    ('demo/rtti.js', "'string'\n'integer'\n"),
    ('demo/overloading.js', "6\n'test'\n36\n'testtesttest'\n'testtest'\n"),
    ('demo/for-loop.js', "0\n1\n2\n3\n4\n5\n6\n7\n8\n9\n"),
    ('demo/recursion.js', "0\n1\n1\n2\n3\n5\n8\n13\n21\n"),
    ('demo/functional.js', "9\n20\n"),
    ('demo/closure.js', "0\n5\n"),
    ('demo/prototype.js', "'dance'\n'dance'\n'swing'\n"),
    ('demo/constant.js', "3\n9\n7\n'abcdef'\n1\n10\n"),
    ('demo/unreachable.js', "'1'\n'2'\n'3'\n")
])
def test_demo(capsys, source, result):
    with open(source, 'r') as f:
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
        assert out == result
