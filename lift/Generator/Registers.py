import sys


registers = [i for i in range(32)]


def sp():
    return 32


def fp():
    return 33


def allocate(num):
    ret = []
    for j in range(num):
        try:
            ret.append(registers.pop())
        except IndexError as e:
            print 'Error occurs during allocating registers.'
            print e
            sys.exit(1)
    return ret


def free(regs):
    for j in regs:
        if j in registers:
            print 'Error occurs during freeing registers.\n' \
                  'The same register is already freed.\n'
            sys.exit(1)
        registers.append(j)
