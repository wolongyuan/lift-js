import pprint
import re
import math
import traceback
import time

import Memory
import Parser
import Labels
import Constants
import Processor
import Registers
import Profiler
import JIT


def run():
    Processor.init()
    try:
        while True:
            pc = Processor.read_pc()
            content = Memory.read(pc)
            assert content['type'] == 2, 'Following content %s is unexpected.' % str(content)
            inst = content['inst']

            Profiler.count(pc)

            if JIT.is_acceleratable(pc):
                JIT.accelerate(pc)
            else:
                """
                print 'Current PC is 0x%08X.' % Processor.read_pc()
                print inst
                """
                Processor.execute(inst)
                JIT.snapshot(pc)
    except KeyboardInterrupt:
        pass
    except:
        print traceback.print_exc()
        print 'Current PC is 0x%08X.' % Processor.read_pc()
        print 'Current instruction is %s.' % str(inst)


def load_text(text):
    addr = 0
    for line in text:
        if line.startswith(';'):
            continue
        if line.find(':') == -1:
            inst = Parser.inst(line)
            Memory.write(addr, {'type': 2, 'inst': inst})
            Profiler.record(addr, inst)
            addr += 4
        else:
            Labels.add(line.strip().split(':')[0], addr)


def load_data(data):
    addr = 0x10000000
    line = 0
    while line < len(data):
        label = data[line].strip().split(':')[0]
        Labels.add(label, addr)
        if label.startswith('int_'):
            value = int(re.match(r'\s+\.word\s+(-?\w+)', data[line+2]).group(1), 16)
            Memory.set_int(addr, value)
            Constants.set_int(value, addr)
            addr += 8
            line += 3
        elif label.startswith('str_'):
            string = re.match(r'\s+\.asciiz\s+"([^"]+)"', data[line+3]).group(1)
            string = string.decode('string_escape')
            Memory.set_str(addr, string)
            Constants.set_str(string, addr)
            addr += 8 + math.floor(len(string) / 4 + 1) * 4
            line += 4


def load(src):
    lines = src
    try:
        data_line = lines.index('.data\n')
        text_line = lines.index('.text\n')
        text = lines[text_line+1:data_line]
        data = lines[data_line+1:-1]
    except ValueError as e:
        if 'data' in e.message:
            text, data = lines, []
        elif 'text' in e.message:
            text, data = [], lines
        else:
            raise e
    load_text(text)
    load_data(data)

