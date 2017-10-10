import pprint
import math
import copy
import Constants
import Processor


memory = {}
state = {
    'heap_addr': 0x30000000
}


def alloc(num):
    """
    Allocation memory space with specific size.

    :param num: the size of memory space in bytes.
    :return: the starting address of allocated memory
    """
    ret = state['heap_addr']
    state['heap_addr'] += num
    return ret


def new_obj():
    """
    Allocate space for a new object.

    :return: object address
    """
    addr = alloc(8)
    write(addr, {'type': 1, 'object': {'type': 3, 'data': 0}, 'content': 3})
    write(addr + 4, {'type': 0, 'content': 0})
    return addr


def get_obj(addr):
    """
    Read the object located in 'addr'. If the location is not an object, an AssertionError
    wiil be raised.

    :param addr: object location
    :return: the content of object
    """
    content = read(addr)
    assert content['type'] == 1, 'Following content is not expected. %s' % str(content)
    return copy.deepcopy(content['object'])


def set_obj(addr, obj):
    """
    Fit the object into location 'addr'. The memory content will be modified accordingly.

    :param addr: destination address
    :param obj: object to fit in
    """
    assert 'type' in obj
    assert 'data' in obj
    obj = copy.deepcopy(obj)
    write(addr, {'type': 1, 'object': obj, 'content': obj['type']})
    write(addr + 4, {'type': 0, 'content': obj['data']})


def new_field(obj_addr, str_addr):
    """
    Get a field with name specified by str_addr in object specified by obj_addr.

    :param obj_addr: pointer to the object
    :param str_addr: pointer to the field name string
    :return: pointer to the new property
    """
    key = get_str(str_addr)
    str_addr = new_str(key)
    obj = get_obj(obj_addr)
    addr = obj['data']
    new_prop_addr = new_prop()
    if not addr:  # The object has no property.
        obj['data'] = new_prop_addr
        set_obj(obj_addr, obj)
        set_prop(new_prop_addr, key=str_addr, ptr=0)
        return new_prop_addr
    while True:
        prop = get_prop(addr)
        if get_str(prop['key']) == key:
            raise Exception('The key "%s" already exists.' % key)
        if prop['ptr']:
            addr = prop['ptr']
        else:
            break
    set_prop(addr, ptr=new_prop_addr)
    set_prop(new_prop_addr, key=str_addr, ptr=0)
    return new_prop_addr


def get_field(obj_addr, str_addr):
    """
    Find a field with name specified by str_addr in object specified by obj_addr.

    :param obj_addr: pointer to the object
    :param str_addr: pointer to the field name string
    :return: addr of a property will be returned if found, otherwise 0 will be returned
    """
    key = get_str(str_addr)
    obj = get_obj(obj_addr)
    addr = obj['data']
    if not addr:  # The object has no property.
        return 0
    while True:
        prop = get_prop(addr)
        if get_str(prop['key']) == key:
            return addr
        if prop['ptr']:
            addr = prop['ptr']
        else:
            break
    return 0


def new_prop():
    """
    Allocate space for a new property.

    :return: property address
    """
    addr = alloc(12)
    write(addr, {'type': 3, 'property':{'key': 0, 'value': 0, 'ptr': 0}, 'content': 0})
    write(addr + 4, 0)
    write(addr + 8, 0)
    return addr


def get_prop(addr):
    content = read(addr)
    assert content['type'] == 3, 'Following content %s is unexpected.' % str(content)
    return copy.deepcopy(content['property'])


def set_prop(addr, key=None, value=None, ptr=None):
    content = read(addr)
    assert content['type'] == 3
    assert 'property' in content
    if key:
        key = int(key)
        content['property']['key'] = key
        content['content'] = key
    if value:
        value = int(value)
        content['property']['value'] = value
        write(addr + 4, {'type': 0, 'content': value})
    if ptr:
        ptr = int(ptr)
        content['property']['ptr'] = ptr
        write(addr + 8, {'type': 0, 'content': ptr})
    write(addr, content)


def new_func():
    func_addr = alloc(8)
    prop_addr = alloc(60)
    write(func_addr, {'type': 1, 'object': {'type': 4, 'data': prop_addr}, 'content': 4})
    write(func_addr + 4, {'type': 0, 'content': prop_addr})
    for index, name in enumerate(['address', 'prototype', 'scope', 'outer', 'arguments']):
        next_addr = prop_addr + 12 if index < 4 else 0
        value = new_obj() if name in ['scope', 'arguments', 'prototype'] else 0
        write(prop_addr, {'type': 3,
                          'property': {'key': Constants.get_str(name), 'value': value, 'ptr': next_addr},
                          'content': Constants.get_str(name)})
        write(prop_addr + 4, {'type': 0, 'content': value})
        write(prop_addr + 8, {'type': 0, 'content': next_addr})
        prop_addr = next_addr
    return func_addr


def new_int(val):
    addr = state['heap_addr']
    set_int(addr, val)
    state['heap_addr'] += 8
    return addr


def fill_str(addr, string):
    """
    Fit a string into memory, starting from the given address.

    :param addr: starting address
    :param string: string to fill in
    """
    cur_addr = addr
    string += '\0' * (4 - len(string) % 4)
    for chunk in [list(string)[i:i+4] for i in range(0, len(string), 4)]:
        value = 0
        for char in reversed(chunk):
            value += (value << 8) + ord(char)
        write(cur_addr, {'type': 0, 'content': value})
        cur_addr += 4


def new_str(string):
    addr = state['heap_addr']
    set_str(addr, string)
    state['heap_addr'] += 8 + math.floor(len(string) / 4 + 1) * 4
    return addr


def get_str(addr):
    content = memory[addr]
    assert content['type'] == 1
    assert 'data' in content['object']
    ret = content['object']['data']
    return ret


def set_str(addr, string):
    write(addr, {'type': 1, 'object': {'type': 2, 'data': string}, 'content': 2})
    write_plain(addr + 4, addr + 8)
    fill_str(addr + 8, string)


def get_int(addr):
    content = memory[addr]
    assert content['type'] == 1
    assert 'data' in content['object']
    ret = content['object']['data']
    assert type(ret) == int or type(ret) == float, 'Following content %s is unexpected.' % str(content)
    return ret


def set_int(addr, val):
    write(addr, {'type': 1, 'object': {'type': 0, 'data': val}, 'content': 0})
    write_plain(addr + 4, val)


def read_plain(addr):
    return read(addr)['content']


def read(addr):
    return copy.deepcopy(memory.get(addr, {'type': 0, 'content': 0x00000000}))


def write_plain(addr, content):
    memory[addr] = {'type': 0, 'content': int(content)}


def write(addr, content):
    content = copy.deepcopy(content)
    memory[addr] = content


def print_obj(addr):
    content = read(addr)
    assert content['type'] == 1, 'Following content %s is unexpected.' % str(content)
    obj = copy.deepcopy(content['object'])
    pprint.pprint(convert_obj(obj))


def convert_obj(obj, level=0):
    if level > 4:
        return 'Unreachable object.'
    primitives = {
        0: obj['data'],
        2: obj['data'],
        5: 'null',
        6: 'undefined',
        7: 'Built-in function panel.readInt().',
        8: 'Built-in function panel.readStr().',
        9: 'Built-in function panel.show().'
    }
    if obj['type'] in primitives:
        return primitives[obj['type']]
    else:
        ret = {}
        addr = obj['data']
        while addr:
            prop = get_prop(addr)
            key = convert_obj(get_obj(prop['key']))
            value = convert_obj(get_obj(prop['value']), level + 1) if prop['value'] else 'null'
            ret[key] = value
            addr = prop['ptr']
        return ret


def dump_obj(addr):
    content = read(addr)
    assert content['type'] == 1, 'Following content %s is unexpected.' % str(content)
    obj = copy.deepcopy(content['object'])
    addr = obj['data']
    while addr:
        prop = copy.deepcopy(get_prop(addr))
        prop['key'] = read(prop['key'])
        if prop['value']:
            prop['value'] = read(prop['value'])
        obj[addr] = prop
        addr = prop['ptr']
    pprint.pprint(obj)


def dump():
    pprint.pprint(memory)


def dump_stack(sp=0x20000000):
    for key in memory:
        if sp < key < 0x2FFFFFFF:
            pprint.pprint(read(key))
