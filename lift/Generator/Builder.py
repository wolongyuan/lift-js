import pprint
import Registers
import Constants
import Labels


op = {
    'newfunc': 'newfunc     ',
    'newobj': 'newobj      ',
    'getfield': 'getfield    ',
    'findfield': 'findfield   ',
    'getvar': 'getvar      ',
    'findvar': 'findvar     ',
    'typeof': 'typeof      ',
    'cmp': 'cmp         ',
    'slt': 'slt         ',
    'add': 'add         ',
    'sub': 'sub         ',
    'mul': 'mul         ',
    'div': 'div         ',
    'mod': 'mod         ',
    'and': 'and         ',
    'or': 'or          ',
    'xor': 'xor         ',
    'not': 'not         ',
    'sra': 'sra         ',
    'srl': 'srl         ',
    'sll': 'sll         ',
    'bez': 'bez         ',
    'bnz': 'bnz         ',
    'ld': 'ld          ',
    'st': 'st          ',
    'la': 'la          ',
    'j': 'j           ',
    'jr': 'jr          ',
    'jal': 'jal         ',
    'jalr': 'jalr        ',
    'push': 'push        ',
    'pop': 'pop         ',
    'move': 'move        ',
    'ret': 'ret'
}


class Builder(object):

    def __init__(self):
        self.scope = {}
        self.code_stack = [['.text']]
        self.code = self.code_stack[-1]
        self.context = {}
        self.reg_stack = [None]
        self.regs = self.reg_stack[-1]  # init function does not need to save context

    def save(self, reg):
        if type(self.regs) == list:  # check whether it's None
            if reg not in [Registers.sp(), Registers.fp()] + self.regs:
                self.regs.append(reg)

    def insert_comment(self, comment):
        self.code.append('; %s' % comment)

    def insert_label(self, label):
        self.code.append(label + ':')

    def inst_newfunc(self, rd, label):
        self.save(rd)
        self.code.append('\t%s$%d, %s' % (op['newfunc'], rd, label))

    def inst_newobj(self, rd):
        self.save(rd)
        self.code.append('\t%s$%d' % (op['newobj'], rd))

    def inst_getfield(self, rd, rs, rt):
        self.save(rd)
        self.code.append('\t%s$%d, $%d, $%d' % (op['getfield'], rd, rs, rt))

    def inst_findfield(self, rd, rs, rt):
        self.save(rd)
        self.code.append('\t%s$%d, $%d, $%d' % (op['findfield'], rd, rs, rt))

    def inst_cmp(self, rd, rs, rt):
        self.save(rd)
        self.code.append('\t%s$%d, $%d, $%d' % (op['cmp'], rd, rs, rt))

    def inst_slt(self, rd, rs, rt):
        self.save(rd)
        self.code.append('\t%s$%d, $%d, $%d' % (op['slt'], rd, rs, rt))

    def inst_add(self, rd, rs, rt):
        self.save(rd)
        self.code.append('\t%s$%d, $%d, $%d' % (op['add'], rd, rs, rt))

    def inst_sub(self, rd, rs, rt):
        self.save(rd)
        self.code.append('\t%s$%d, $%d, $%d' % (op['sub'], rd, rs, rt))

    def inst_mul(self, rd, rs, rt):
        self.save(rd)
        self.code.append('\t%s$%d, $%d, $%d' % (op['mul'], rd, rs, rt))

    def inst_div(self, rd, rs, rt):
        self.save(rd)
        self.code.append('\t%s$%d, $%d, $%d' % (op['div'], rd, rs, rt))

    def inst_mod(self, rd, rs, rt):
        self.save(rd)
        self.code.append('\t%s$%d, $%d, $%d' % (op['mod'], rd, rs, rt))

    def inst_and(self, rd, rs, rt):
        self.save(rd)
        self.code.append('\t%s$%d, $%d, $%d' % (op['and'], rd, rs, rt))

    def inst_or(self, rd, rs, rt):
        self.save(rd)
        self.code.append('\t%s$%d, $%d, $%d' % (op['or'], rd, rs, rt))

    def inst_xor(self, rd, rs, rt):
        self.save(rd)
        self.code.append('\t%s$%d, $%d, $%d' % (op['xor'], rd, rs, rt))

    def inst_not(self, rd, rs, rt):
        self.save(rd)
        self.code.append('\t%s$%d, $%d, $%d' % (op['not'], rd, rs, rt))

    def inst_sra(self, rd, rs, rt):
        self.save(rd)
        self.code.append('\t%s$%d, $%d, $%d' % (op['sra'], rd, rs, rt))

    def inst_srl(self, rd, rs, rt):
        self.save(rd)
        self.code.append('\t%s$%d, $%d, $%d' % (op['srl'], rd, rs, rt))

    def inst_sll(self, rd, rs, rt):
        self.save(rd)
        self.code.append('\t%s$%d, $%d, $%d' % (op['sll'], rd, rs, rt))

    def inst_getvar(self, rd, rs):
        self.save(rd)
        self.code.append('\t%s$%d, $%d' % (op['getvar'], rd, rs))

    def inst_findvar(self, rd, rs):
        self.save(rd)
        self.code.append('\t%s$%d, $%d' % (op['findvar'], rd, rs))

    def inst_typeof(self, rd, rs):
        self.save(rd)
        self.code.append('\t%s$%d, $%d' % (op['typeof'], rd, rs))

    def inst_move(self, rd, rs):
        self.save(rd)
        self.code.append('\t%s$%d, $%d' % (op['move'], rd, rs))

    def inst_bez(self, rs, label):
        self.code.append('\t%s$%d, %s' % (op['bez'], rs, label))

    def inst_bnz(self, rs, label):
        self.code.append('\t%s$%d, %s' % (op['bnz'], rs, label))

    def inst_ld(self, rd, rs, offset):
        self.save(rd)
        self.code.append('\t%s$%d, %d($%d)' % (op['ld'], rd, offset, rs))

    def inst_st(self, rd, rs, offset):
        self.code.append('\t%s$%d, %d($%d)' % (op['st'], rd, offset, rs))

    def inst_la(self, rd, label):
        self.save(rd)
        self.code.append('\t%s$%d, %s' % (op['la'], rd, label))

    def inst_j(self, label):
        self.code.append('\t%s%s' % (op['j'], label))

    def inst_jalr(self, rd):
        self.save(rd)
        self.code.append('\t%s$%d' % (op['jalr'], rd))

    def inst_ret(self):
        self.code.append('\t%s' % op['ret'])

    def push(self, rd):
        sp = Registers.sp()
        self.inst_st(rd, sp, 0)
        self.inst_la(rd, Constants.integer(4))  # reuse rd so as not to introduce new register
        self.inst_sub(sp, sp, rd)
        self.inst_ld(rd, sp, 4)

    def pop(self, rd):
        sp = Registers.sp()
        self.inst_la(rd, Constants.integer(4))  # reuse rd so as not to introduce new register
        self.inst_add(sp, sp, rd)
        self.inst_ld(rd, sp, 0)

    def call_func(self, func, this, args):
        fp = Registers.fp()
        sp = Registers.sp()
        temp, zero = Registers.allocate(2)
        self.inst_newobj(temp)
        self.inst_la(zero, Constants.integer(0))
        self.inst_add(temp, fp, zero)
        self.push(temp)  # push fp
        Registers.free([temp, zero])
        self.inst_move(fp, sp)
        self.push(0)  # dummy push for return address
        self.push(func)
        self.push(this)
        self.push(0)  # dummy push for return value
        for arg in args:
            self.push(arg)
        self.inst_jalr(func)

    def get_ret(self, rd):
        """
        Get return value after a function call. Also, it modifies fp and sp accordingly.

        :param rd: register to store the value
        """
        self.inst_ld(rd, Registers.fp(), -12)  # get return value
        self.inst_move(Registers.sp(), Registers.fp())  # reset stack pointer
        self.pop(Registers.fp())
        # self.inst_ld(Registers.fp(), Registers.fp(), 4)  # get previous fp

    def get_this(self, rd):
        self.inst_ld(rd, Registers.fp(), -8)

    def enter(self, func):
        self.code_stack.append([])
        self.scope[func] = self.code_stack[-1]
        self.code = self.code_stack[-1]
        self.reg_stack.append([])
        self.context[func] = self.reg_stack[-1]
        self.regs = self.reg_stack[-1]

    def exit(self, func):
        try:
            while True:
                self.code_stack[-1].remove('\tret')  # remove trailing 'ret' instruction
        except ValueError:
            pass
        # save all used registers
        self.code = []
        for reg in reversed(self.regs):
            self.push(reg)
        for inst in reversed(self.code):
            self.code_stack[-1].insert(0, inst)
        # restore all used registers
        self.code = []
        for reg in self.regs:
            self.pop(reg)
        for inst in self.code:
            self.code_stack[-1].append(inst)
        self.code_stack[-1].append('\tret')  # add 'ret' instruction
        self.code_stack.pop()
        self.code = self.code_stack[-1]
        self.reg_stack.pop()
        self.regs = self.reg_stack[-1]

    def halt(self):
        temp = Labels.temp()
        self.insert_label(temp)
        self.inst_j(temp)

    def dump(self):
        main = '\n'.join(self.code)
        functions = '\n'.join([func + ':\n' + '\n'.join(self.scope[func]) for func in self.scope])
        return '\n'.join([main, functions]) if functions else main  # prevent blank line if there is no function
