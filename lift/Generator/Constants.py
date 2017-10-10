import Util
import math
import pprint
import bitstring


string_pool = {}
integer_pool = {}
start_address = 0x10000000  # the start_address of data section


def string(str):
    if str in string_pool:
        return string_pool[str]
    else:
        label = 'str_' + Util.rand_bytes()
        string_pool[str] = label
        return label


def integer(num):
    if num in integer_pool:
        return integer_pool[num]
    else:
        if num >= 0:
            label = 'int_%d' % (num,)
        else:
            label = 'int_%s' % (bitstring.Bits(int=num, length=32).hex,)
        integer_pool[num] = label
        return label


def dump():
    addr = start_address
    ret = '\n.data\n'
    for (text, label) in string_pool.iteritems():
        ret += '{label}:\n\t.word\t0x2\n\t.word\t{addr}\n\t.asciiz\t"{str}"\n'.format(
            label=label, addr=hex(addr+8), str=text.encode('string_escape')
        )
        addr += int(math.ceil((len(text) + 1) / 4.0) * 4 + 8)
    for (num, label) in integer_pool.iteritems():
        ret += '{label}:\n\t.word\t0x0\n\t.word\t{num}\n'.format(
            label=label, num=hex(num)
        )
        addr += 8
    ret += '\n'
    return ret
