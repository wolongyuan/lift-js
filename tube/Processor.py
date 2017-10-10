import pprint
import Constants
import Memory
import Registers
import Labels


state = {'pc': 0, 'prev_pc': 0, 'count': 0, 'init_func': 0}


def read_pc():
    return state['pc']


def write_pc(pc):
    state['prev_pc'] = state['pc']
    state['pc'] = pc
    state['count'] = state['count'] + 1 if state['prev_pc'] == state['pc'] else 0
    if state['count'] > 1:  # The program has been here for more than 20 times.
        raise KeyboardInterrupt()  # Terminate the program.


def inc_pc(inc):
    write_pc(read_pc() + inc)


def init():
    for name in ['constructor', 'prototype', 'this', 'address', 'scope', 'outer', 'null', 'undefined',
                 'panel', 'readStr', 'readInt', 'integer', 'object', 'function', 'arguments']:
        Constants.get_str(name)

    for value in [1, 4]:
        Constants.get_int(value)

    addr = Memory.alloc(8)
    Memory.write(addr, {'type': 1, 'content': 5, 'object': {'type': 5}})  # null
    Constants.set_special('null', addr)

    addr = Memory.alloc(8)
    Memory.write(addr, {'type': 1, 'content': 6, 'object': {'type': 6}})  # undefined
    Constants.set_special('undefined', addr)

    Registers.set_sp(Memory.new_int(0x2FFFFFFC))  # sp
    Registers.set_fp(Memory.new_int(0x2FFFFFFC))  # fp

    # initialize runtime stack
    init_func = Memory.new_func()  # function 'init
    state['init_func'] = init_func
    fp_addr = Memory.get_int(Registers.get_fp())
    Memory.write_plain(fp_addr, 0)  # return address
    Memory.write_plain(fp_addr - 4, init_func)  # current function
    Memory.write_plain(fp_addr - 8, Memory.new_obj())  # this pointer
    Memory.write_plain(fp_addr - 12, 0)  # return value
    Memory.set_int(Registers.get_sp(), fp_addr - 16)

    # add function 'Object' into 'init'
    scope_field = Memory.get_field(init_func, Constants.get_str('scope'))
    scope_addr = Memory.get_prop(scope_field)['value']
    object_field = Memory.new_field(scope_addr, Constants.get_str('Object'))
    object_addr = Memory.new_obj()
    Memory.set_prop(object_field, value=object_addr)
    state['obj_func'] = object_addr

    # add object 'panel' into 'init'
    panel_field = Memory.new_field(scope_addr, Constants.get_str('panel'))
    panel_addr = Memory.new_obj()
    Memory.set_prop(panel_field, value=panel_addr)

    # add property 'readInt' into 'panel'
    read_int_prop = Memory.new_field(panel_addr, Constants.get_str('readInt'))
    read_int_func = Memory.new_func()
    Memory.set_prop(read_int_prop, value=read_int_func)
    read_int_obj = Memory.get_obj(read_int_func)
    read_int_obj['type'] = 7  # special type value
    Memory.set_obj(read_int_func, read_int_obj)

    # add property 'readStr' into 'panel'
    read_str_prop = Memory.new_field(panel_addr, Constants.get_str('readStr'))
    read_str_func = Memory.new_func()
    Memory.set_prop(read_str_prop, value=read_str_func)
    read_str_obj = Memory.get_obj(read_str_func)
    read_str_obj['type'] = 8
    Memory.set_obj(read_str_func, read_str_obj)

    # add property 'show' into 'panel'
    show_prop = Memory.new_field(panel_addr, Constants.get_str('show'))
    show_func = Memory.new_func()
    Memory.set_prop(show_prop, value=show_func)
    show_obj = Memory.get_obj(show_func)
    show_obj['type'] = 9
    Memory.set_obj(show_func, show_obj)


def exec_la(inst):
    Registers.set_reg(inst['rd'], Labels.query(inst['label']))
    inc_pc(4)


def exec_ld(inst):
    src_addr = Memory.get_int(Registers.get_reg(inst['rs'])) + inst['offset']
    Registers.set_reg(inst['rd'], Memory.read_plain(src_addr))
    inc_pc(4)


def exec_st(inst):
    dest_addr = Memory.get_int(Registers.get_reg(inst['rs'])) + inst['offset']
    Memory.write_plain(dest_addr, Registers.get_reg(inst['rd']))
    inc_pc(4)


def exec_move(inst):
    rd_val = Registers.get_reg(inst['rd'])
    rs_val = Registers.get_reg(inst['rs'])
    Memory.set_obj(rd_val, Memory.get_obj(rs_val))
    inc_pc(4)


def exec_sub(inst):
    rs_val = Memory.get_int(Registers.get_reg(inst['rs']))
    rt_val = Memory.get_int(Registers.get_reg(inst['rt']))
    Memory.set_int(Registers.get_reg(inst['rd']), rs_val - rt_val)
    inc_pc(4)


def exec_getvar(inst):
    func_addr = Memory.read_plain(Registers.read_fp() - 4)
    rs_val = Registers.get_reg(inst['rs'])
    while True:
        arg_field = Memory.get_field(func_addr, Constants.get_str('arguments'))
        arg_obj = Memory.get_prop(arg_field)['value']
        var_field = Memory.get_field(arg_obj, rs_val)
        if var_field:  # The field is found in arguments.
            offset_addr = Memory.get_prop(var_field)['value']
            offset = Memory.get_int(offset_addr)
            Registers.set_reg(inst['rd'], Memory.read_plain(Registers.read_fp() + offset))
            break
        scope_field = Memory.get_field(func_addr, Constants.get_str('scope'))
        scope_obj = Memory.get_prop(scope_field)['value']
        var_field = Memory.get_field(scope_obj, rs_val)
        if var_field:  # The field is found in scope.
            var_obj = Memory.get_prop(var_field)['value']
            Registers.set_reg(inst['rd'], var_obj)
            break
        outer_field = Memory.get_field(func_addr, Constants.get_str('outer'))
        outer_obj = Memory.get_prop(outer_field)['value']
        if not outer_obj:  # The field 'outer' is empty.
            func_addr = Memory.read_plain(Registers.read_fp() - 4)
            scope_field = Memory.get_field(func_addr, Constants.get_str('scope'))
            scope_obj = Memory.get_prop(scope_field)['value']
            prop_addr = Memory.new_field(scope_obj, rs_val)
            obj_addr = Memory.new_obj()
            Memory.set_prop(prop_addr, value=obj_addr)
            Registers.set_reg(inst['rd'], obj_addr)
            break
        else:
            func_addr = outer_obj
    inc_pc(4)


def exec_getfield(inst):
    name_addr = Registers.get_reg(inst['rt'])
    obj_addr = Registers.get_reg(inst['rs'])
    while True:
        try:
            field = Memory.get_field(obj_addr, name_addr)
        except Exception as e:
            Memory.print_obj(obj_addr)
            Memory.print_obj(name_addr)
            raise e
        if not field:  # The field cannot be found.
            ctor_addr = Memory.get_field(obj_addr, Constants.get_str('constructor'))
            if not ctor_addr:  # There is no constructor field
                new_field = Memory.new_field(Registers.get_reg(inst['rs']), name_addr)
                Memory.set_prop(new_field, value=Memory.new_obj())
                res = Memory.get_prop(new_field)
                break
            ctor_obj = Memory.get_prop(ctor_addr)['value']
            proto_addr = Memory.get_field(ctor_obj, Constants.get_str('prototype'))
            if not proto_addr:  # There is no prototype field
                new_field = Memory.new_field(Registers.get_reg(inst['rs']), name_addr)
                Memory.set_prop(new_field, value=Memory.new_obj())
                res = Memory.get_prop(new_field)
                break
            obj_addr = Memory.get_prop(proto_addr)['value']  # Find field in the prototype
        else:
            res = Memory.get_prop(field)
            break
    Registers.set_reg(inst['rd'], res['value'])
    inc_pc(4)
    """
    # rs_val = Registers.get_reg(inst['rs'])
    # rt_val = Registers.get_reg(inst['rt'])
    field = Memory.get_field(rs_val, rt_val)
    if not field:  # The field cannot be found.
        pass  # TODO: find field along prototype chain.
        new_field = Memory.new_field(rs_val, rt_val)
        Memory.set_prop(new_field, value=Memory.new_obj())
        res = Memory.get_prop(new_field)
    else:
        res = Memory.get_prop(field)
    Registers.set_reg(inst['rd'], res['value'])
    inc_pc(4)
    """


def exec_jalr(inst):
    Memory.write_plain(Registers.read_fp(), read_pc())  # set return address
    func_obj = Memory.get_obj(Registers.get_reg(inst['rd']))
    if func_obj['type'] == 7:  # panel.readInt()
        num = int(raw_input('Please enter an integer.\n'))
        num_addr = Memory.new_int(num)
        Memory.write_plain(Registers.read_fp() - 12, num_addr)
        inc_pc(4)
    elif func_obj['type'] == 8:  # panel.readStr()
        string = raw_input('Please enter an string.\n')
        str_addr = Memory.new_str(string)
        Memory.write_plain(Registers.read_fp() - 12, str_addr)
        inc_pc(4)
    elif func_obj['type'] == 9:  # panel.show()
        arg = Memory.read_plain(Registers.read_fp() - 16)
        Memory.print_obj(arg)
        inc_pc(4)
    else:
        assert func_obj['type'] == 4
        func_addr = Registers.get_reg(inst['rd'])
        address_field = Memory.get_field(func_addr, Constants.get_str('address'))
        address_addr = Memory.get_prop(address_field)['value']
        address = Memory.get_int(address_addr)
        Memory.write_plain(Registers.read_fp(), read_pc() + 4)
        write_pc(address)


def exec_newobj(inst):
    Registers.set_reg(inst['rd'], Memory.new_obj())
    inc_pc(4)


def exec_add(inst):
    rs_obj = Memory.get_obj(Registers.get_reg(inst['rs']))
    rt_obj = Memory.get_obj(Registers.get_reg(inst['rt']))
    rd_val = Registers.get_reg(inst['rd'])
    if rs_obj['type'] == 0 and rt_obj['type'] == 0:  # both are integers
        Memory.set_int(rd_val, rs_obj['data'] + rt_obj['data'])
    elif rs_obj['type'] == 3 and rs_obj['data'] == 0:  # rs references an empty object
        Memory.set_obj(rd_val, rt_obj)
    elif rt_obj['type'] == 3 and rt_obj['data'] == 0:  # rt references an empty object
        Memory.set_obj(rd_val, rs_obj)
    elif rs_obj['type'] == 2 and rt_obj['type'] == 2:  # both are strings
        str_addr = Memory.new_str(rs_obj['data'] + rt_obj['data'])
        Memory.set_obj(rd_val, Memory.get_obj(str_addr))
    # TODO: more cases in addition
    inc_pc(4)


def exec_mul(inst):
    rs_obj = Memory.get_obj(Registers.get_reg(inst['rs']))
    rt_obj = Memory.get_obj(Registers.get_reg(inst['rt']))
    rd_val = Registers.get_reg(inst['rd'])
    if rs_obj['type'] == 0 and rt_obj['type'] == 0:  # both are integers
        Memory.set_int(rd_val, rs_obj['data'] * rt_obj['data'])
    elif {rs_obj['type'], rt_obj['type']} == {0, 2}:  # an integer and a string
        str_addr = Memory.new_str(rs_obj['data'] * rt_obj['data'])
        Memory.set_obj(rd_val, Memory.get_obj(str_addr))
    inc_pc(4)


def exec_typeof(inst):
    obj = Memory.get_obj(Registers.get_reg(inst['rs']))
    types = {
        0: 'integer',
        2: 'string',
        3: 'object',
        4: 'function',
        5: 'null',
        6: 'undefined',
        7: 'function',
        8: 'function',
        9: 'function'
    }
    res = types[obj['type']]
    Registers.set_reg(inst['rd'], Constants.get_str(res))
    inc_pc(4)


def exec_j(inst):
    write_pc(Labels.query(inst['label']))


def exec_cmp(inst):
    rs_obj = Memory.get_obj(Registers.get_reg(inst['rs']))
    rt_obj = Memory.get_obj(Registers.get_reg(inst['rt']))
    if rs_obj['type'] == rt_obj['type'] and rs_obj['data'] == rt_obj['data']:
        Registers.set_reg(inst['rd'], Constants.get_int(1))
    else:
        Registers.set_reg(inst['rd'], Constants.get_int(0))
    inc_pc(4)


def exec_slt(inst):
    rs_obj = Memory.get_obj(Registers.get_reg(inst['rs']))
    rt_obj = Memory.get_obj(Registers.get_reg(inst['rt']))
    if (rs_obj['type'] == 0 and rt_obj['type'] == 0) or \
       (rs_obj['type'] == 2 and rt_obj['type'] == 2):
        if rs_obj['data'] < rt_obj['data']:
           Registers.set_reg(inst['rd'], Constants.get_int(1))
        else:
            Registers.set_reg(inst['rd'], Constants.get_int(0))
    else:
        raise Exception('The following object are not comparable yet.\n' +
                        '%s\n%s' % (str(rs_obj), str(rt_obj)))
    inc_pc(4)


def is_true(obj):
    if obj['type'] == 0:  # the object is an interger
        return obj['data'] != 0
    elif obj['type'] == 2:  # the object is a string
        return obj['data'] != ''
    elif obj['type'] == 3:  # the object is an object
        return obj['data'] != 0  # check whether it's an empty object
    elif obj['type'] == 5:  # null
        return False
    elif obj['type'] == 6:  # undefined
        return False
    else:  # the object is a function
        return True


def exec_bez(inst):
    rs_obj = Memory.get_obj(Registers.get_reg(inst['rs']))
    if not is_true(rs_obj):
        write_pc(Labels.query(inst['label']))
    else:
        inc_pc(4)


def exec_bnz(inst):
    rs_obj = Memory.get_obj(Registers.get_reg(inst['rs']))
    if is_true(rs_obj):
        write_pc(Labels.query(inst['label']))
    else:
        inc_pc(4)


def exec_newfunc(inst):
    func_addr = Memory.new_func()
    address_prop = Memory.get_field(func_addr, Constants.get_str('address'))
    Memory.set_prop(address_prop, value=Memory.new_int(Labels.query(inst['label'])))
    outer_func = Memory.read_plain(Registers.read_fp() - 4)
    outer_prop = Memory.get_field(func_addr, Constants.get_str('outer'))
    Memory.set_prop(outer_prop, value=outer_func)
    Registers.set_reg(inst['rd'], func_addr)
    inc_pc(4)


def exec_ret(inst):
    ret_addr = Memory.read_plain(Registers.read_fp())
    write_pc(ret_addr)


executors = {
    'la': exec_la,
    'ld': exec_ld,
    'st': exec_st,
    'move': exec_move,
    'sub': exec_sub,
    'add': exec_add,
    'getfield': exec_getfield,
    'getvar': exec_getvar,
    'jalr': exec_jalr,
    'typeof': exec_typeof,
    'newobj': exec_newobj,
    'j': exec_j,
    'mul': exec_mul,
    'cmp': exec_cmp,
    'slt': exec_slt,
    'bez': exec_bez,
    'bnz': exec_bnz,
    'newfunc': exec_newfunc,
    'ret': exec_ret
}


def execute(inst):
    executors[inst['type']](inst)
