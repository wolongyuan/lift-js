import re

inst_regex = {
    'newfunc': r'\s+(?P<type>\w+)\s+\$(?P<rd>\d+),\s+(?P<label>\w+)',
    'newobj': r'\s+(?P<type>\w+)\s+\$(?P<rd>\d+)',
    'getfield': r'\s+(?P<type>\w+)\s+\$(?P<rd>\d+),\s+\$(?P<rs>\d+),\s+\$(?P<rt>\d+)',
    'findfield': r'\s+(?P<type>\w+)\s+\$(?P<rd>\d+),\s+\$(?P<rs>\d+),\s+\$(?P<rt>\d+)',
    'getvar': r'\s+(?P<type>\w+)\s+\$(?P<rd>\d+),\s+\$(?P<rs>\d+)',
    'findvar': r'\s+(?P<type>\w+)\s+\$(?P<rd>\d+),\s+\$(?P<rs>\d+)',
    'typeof': r'\s+(?P<type>\w+)\s+\$(?P<rd>\d+),\s+\$(?P<rs>\d+)',
    'cmp': r'\s+(?P<type>\w+)\s+\$(?P<rd>\d+),\s+\$(?P<rs>\d+),\s+\$(?P<rt>\d+)',
    'slt': r'\s+(?P<type>\w+)\s+\$(?P<rd>\d+),\s+\$(?P<rs>\d+),\s+\$(?P<rt>\d+)',
    'add': r'\s+(?P<type>\w+)\s+\$(?P<rd>\d+),\s+\$(?P<rs>\d+),\s+\$(?P<rt>\d+)',
    'sub': r'\s+(?P<type>\w+)\s+\$(?P<rd>\d+),\s+\$(?P<rs>\d+),\s+\$(?P<rt>\d+)',
    'mul': r'\s+(?P<type>\w+)\s+\$(?P<rd>\d+),\s+\$(?P<rs>\d+),\s+\$(?P<rt>\d+)',
    'div': r'\s+(?P<type>\w+)\s+\$(?P<rd>\d+),\s+\$(?P<rs>\d+),\s+\$(?P<rt>\d+)',
    'mod': r'\s+(?P<type>\w+)\s+\$(?P<rd>\d+),\s+\$(?P<rs>\d+),\s+\$(?P<rt>\d+)',
    'and': r'\s+(?P<type>\w+)\s+\$(?P<rd>\d+),\s+\$(?P<rs>\d+),\s+\$(?P<rt>\d+)',
    'or': r'\s+(?P<type>\w+)\s+\$(?P<rd>\d+),\s+\$(?P<rs>\d+),\s+\$(?P<rt>\d+)',
    'xor': r'\s+(?P<type>\w+)\s+\$(?P<rd>\d+),\s+\$(?P<rs>\d+),\s+\$(?P<rt>\d+)',
    'not': r'\s+(?P<type>\w+)\s+\$(?P<rd>\d+),\s+\$(?P<rs>\d+)',
    'sra': r'\s+(?P<type>\w+)\s+\$(?P<rd>\d+),\s+\$(?P<rs>\d+),\s+\$(?P<rt>\d+)',
    'srl': r'\s+(?P<type>\w+)\s+\$(?P<rd>\d+),\s+\$(?P<rs>\d+),\s+\$(?P<rt>\d+)',
    'sll': r'\s+(?P<type>\w+)\s+\$(?P<rd>\d+),\s+\$(?P<rs>\d+),\s+\$(?P<rt>\d+)',
    'bez': r'\s+(?P<type>\w+)\s+\$(?P<rs>\d+),\s+(?P<label>\w+)',
    'bnz': r'\s+(?P<type>\w+)\s+\$(?P<rs>\d+),\s+(?P<label>\w+)',
    'ld': r'\s+(?P<type>\w+)\s+\$(?P<rd>\d+),\s+(?P<offset>-?\d+)\(\$(?P<rs>\d+)\)',
    'st': r'\s+(?P<type>\w+)\s+\$(?P<rd>\d+),\s+(?P<offset>-?\d+)\(\$(?P<rs>\d+)\)',
    'la': r'\s+(?P<type>\w+)\s+\$(?P<rd>\d+),\s+(?P<label>\w+)',
    'j': r'\s+(?P<type>\w+)\s+(?P<label>\w+)',
    'jr': r'\s+(?P<type>\w+)\s+\$(?P<rd>\d+)',
    'jalr': r'\s+(?P<type>\w+)\s+\$(?P<rd>\d+)',
    'move': r'\s+(?P<type>\w+)\s+\$(?P<rd>\d+),\s+\$(?P<rs>\d+)',
    'ret': r'\s+(?P<type>\w+)'
}


def inst(text):
    """
    Parse an instruction and return a dict representing it.

    >>> inst('newfunc $1, label')
    {type: 'newfunc', rd: 1, label: 'label'}

    :param text: instruction text
    :return: a dict corresponding to the instruction
    """
    fields = text.split()
    regex = inst_regex[fields[0]]
    res = re.match(regex, text).groupdict()
    for key in ['rd', 'rs', 'rt', 'offset']:
        if key in res:
            res[key] = int(res[key])
    return res
