import Memory


string_pool = {}
integer_pool = {}
special_pool = {}


def set_str(string, addr):
    string_pool[string] = addr


def get_str(string):
    if string in string_pool:
        return string_pool[string]
    else:
        addr = Memory.new_str(string)
        string_pool[string] = addr
        return addr


def set_int(value, addr):
    integer_pool[value] = addr


def get_int(value):
    if value in integer_pool:
        return integer_pool[value]
    else:
        addr = Memory.new_int(value)
        integer_pool[value] = addr
        return addr


def set_special(name, addr):
    special_pool[name] = addr


def get_special(name):
    return special_pool[name]
