import Memory


# 32 -> sp, 33 -> fp
regs = [0 for i in range(34)]
SP = 32
FP = 33


def sp():
    return SP


def read_sp():
    return Memory.get_int(regs[SP])


def write_sp(val):
    Memory.set_int(regs[SP], val)


def get_sp():
    return regs[SP]


def set_sp(content):
    regs[SP] = content


def fp():
    return FP


def read_fp():
    return Memory.get_int(regs[FP])


def write_fp(val):
    Memory.set_int(regs[FP], val)


def get_fp():
    return regs[FP]


def set_fp(content):
    regs[FP] = content


def get_reg(num):
    return regs[num]


def set_reg(num, content):
    if num in [SP, FP]:
        Memory.get_int(content)  # check whether it points to an integer
    regs[num] = content
