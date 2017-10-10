import copy
import pprint
import Registers
import Processor


optimizable = ['typeof', 'la', 'getvar', 'findvar', 'getfield', 'findfield']
shortpaths = {}
state = {'cur': -1, 'block': None, 'records': {}}


def snapshot(pc):
    cur = state['cur']
    if cur == -1:
        return
    records = state['records']
    if pc == state['block']['exit']: # all infomation has been collected
        fixed = [False for i in range(34)]  # recording whether the register value is fixed
        for index in sorted(records):  # search for constants
            inst = records[index]['inst']
            rd = inst['rd']
            if inst['type'] == 'la':
                records[index]['freeze'] = True
                fixed[rd] = True
            elif inst['type'] in ['typeof', 'getvar']:
                if fixed[inst['rs']]:
                    records[index]['freeze'] = True
                    fixed[rd] = True
            elif inst['type'] == 'getfield':
                if fixed[inst['rs']] and fixed[inst['rt']]:
                    records[index]['freeze'] = True
                    fixed[rd] = True
            else:
                fixed[rd] = False
        shortpath = None
        for index in sorted(records):
            rd = records[index]['inst'].get('rd', 0)
            rd_val = records[index].get('rd', 0)
            frozen = records[index].get('freeze', False)
            if shortpath is None:
                if frozen:
                    shortpath = {'regs': {rd: rd_val}}
                    shortpaths[index] = shortpath
            else:
                if frozen:
                    shortpath['regs'][rd] = rd_val
                else:
                    shortpath['exit'] = index
                    shortpath = None
        # pprint.pprint(shortpaths)
        # raise Exception()
        state['cur'] = -1
        state['block'] = None
        state['records'] = {}
    else:
        record = {'inst': state['block']['insts'].pop()}
        if record['inst']['type'] in optimizable:
            record['rd'] = Registers.get_reg(record['inst']['rd'])
        records[pc] = record


def optimize(pc, block):
    # print pc
    # pprint.pprint(block)
    state['block'] = copy.deepcopy(block)
    state['block']['insts'].reverse()
    state['cur'] = pc


def accelerate(pc):
    shortpath = shortpaths[pc]
    for reg in shortpath['regs']:
        Registers.set_reg(reg, shortpath['regs'][reg])
    Processor.write_pc(shortpath['exit'])


def is_acceleratable(pc):
    return pc in shortpaths
