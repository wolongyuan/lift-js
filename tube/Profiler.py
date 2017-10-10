import pprint
import JIT


blocks = {}
counter = {}
state = {'cur': -1}


breakable = ['j', 'jalr', 'ret', 'bez', 'bnz']


def record(pc, inst):
    if state['cur'] == -1:
        if inst['type'] not in breakable:
            state['cur'] = pc
            blocks[pc] = {'insts': [inst]}
            counter[pc] = 0
    else:
        if inst['type'] in breakable:
            blocks[state['cur']]['exit'] = pc
            state['cur'] = -1
        else:
            blocks[state['cur']]['insts'].append(inst)


def count(pc):
    if pc in blocks:
        counter[pc] += 1
        # TODO: call JIT if it's hot
        if counter[pc] >= 480:
            JIT.optimize(pc, blocks[pc])
            del counter[pc]
            del blocks[pc]
