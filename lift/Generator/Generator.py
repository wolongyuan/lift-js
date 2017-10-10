"""
Code generator for Lift JS.
"""
from Builder import Builder
import Registers
import Constants
import Labels
import pprint


builder = Builder()
context = {
    'function': []
}


def gen_string_literal(string):
    label = Constants.string(string)
    rd = Registers.allocate(1)[0]
    builder.inst_la(rd, label)
    return rd


def gen_literal(ast):
    assert ast[0] == 'Literal'
    if type(ast[1]) == int:
        label = Constants.integer(ast[1])
        rd = Registers.allocate(1)[0]
        builder.inst_la(rd, label)
        return rd
    elif type(ast[1]) == str:
        return gen_string_literal(ast[1])
    elif type(ast[1]) == bool:
        label = Constants.integer(1 if ast[1] else 0)
        rd = Registers.allocate(1)[0]
        builder.inst_la(rd, label)
        return rd
    # TODO: more literal types


def gen_identifier(ast, as_literal=False):
    assert ast[0] == 'Identifier'
    ret = Registers.allocate(1)[0]
    builder.inst_la(ret, Constants.string(ast[1]))
    if not as_literal:
        builder.inst_getvar(ret, ret)  # TODO: getvar/findvar?
    return ret


def gen_function_body(ast):
    assert ast[0] == 'FunctionBody'
    if ast[2] != '}':
        gen_statement_list(ast[2])
    builder.inst_ret()


def gen_function_expression(ast):
    assert ast[0] == 'FunctionExpression'
    label = Labels.function()
    func, temp = Registers.allocate(2)
    builder.inst_newfunc(func, label)
    context['function'].append(func)
    if ast[2] != '(':
        # The function has an identifier
        identifier = gen_identifier(ast[2], True)
        builder.inst_getvar(temp, identifier)
        builder.inst_move(temp, func)
        Registers.free([identifier])
    args, t1, t2 = Registers.allocate(3)
    builder.inst_la(t1, Constants.string('arguments'))
    builder.inst_getfield(args, func, t1)
    if ast[-3] != '(':
        # The function has arguments
        offset = -16
        for node in ast[-3]:
            if type(node) == list:
                arg = gen_identifier(node, True)
                builder.inst_getfield(t1, args, arg)
                builder.inst_la(t2, Constants.integer(offset))
                builder.inst_move(t1, t2)
                Registers.free([arg])
                offset -= 4
    Registers.free([t1, t2])
    # The function body starts.
    builder.enter(label)
    gen_function_body(ast[-1])
    builder.exit(label)
    context['function'].pop()
    return func


def gen_property_name(ast):
    assert ast[0] == 'PropertyName', str(ast)
    if type(ast[1]) == list:  # identifier
        return gen_identifier(ast[1], True)
    elif type(ast[1]) == str:  # string literal
        return gen_string_literal(ast[1])
    # TODO: more type of property


def gen_object_literal(ast):
    assert ast[0] == 'ObjectLiteral', str(ast)
    obj = Registers.allocate(1)[0]
    builder.inst_newobj(obj)
    for node in ast[2]:
        if type(node) != list:
            continue
        key = gen_property_name(node[1])
        value = gen_assignment_expression_no_in(node[3])
        builder.inst_getfield(key, obj, key)
        builder.inst_move(key, value)
        Registers.free([key, value])
    return obj


def gen_primary_expression(ast):
    assert ast[0] == 'PrimaryExpression'
    if ast[1] == 'this':
        this = Registers.allocate(1)[0]
        builder.get_this(this)
        return this
    elif ast[1][0] == 'Literal':
        return gen_literal(ast[1])
    elif ast[1][0] == 'Identifier':
        return gen_identifier(ast[1])
    elif ast[1][0] == 'FunctionExpression':
        return gen_function_expression(ast[1])
    elif ast[1][0] == 'ObjectLiteral':
        return gen_object_literal(ast[1])
    # TODO
    pass


def gen_allocation_expression(ast):
    assert ast[0] == 'AllocationExpression'
    func = gen_member_expression(ast[2])  # it should be a function
    args = []
    if ast[3][-2] != '(':  # there are some arguments
        for node in ast[3][-2]:
            if type(node) == list:
                args.append(gen_assignment_expression_no_in(node))
    this = Registers.allocate(1)[0]
    builder.inst_newobj(this)
    builder.call_func(func, this, args)
    Registers.free([this] + args)
    ret, temp = Registers.allocate(2)
    builder.get_this(ret)
    builder.get_ret(temp)  # temp will be discarded immediately
    builder.inst_la(temp, Constants.string('constructor'))
    builder.inst_getfield(temp, ret, temp)
    builder.inst_move(temp, func)
    Registers.free([temp, func])
    return ret


def gen_member_expression_part(ast):
    assert ast[0] == 'MemberExpressionPart'
    if ast[1] == '[':
        return gen_expression_no_in(ast[2])
    elif ast[1] == '.':
        return gen_identifier(ast[2], True)


def gen_member_expression(ast):
    assert ast[0] == 'MemberExpression'
    if ast[1][0] == 'PrimaryExpression':
        return gen_primary_expression(ast[1])
    elif ast[1][0] == 'MemberExpression':
        obj = gen_member_expression(ast[1])
        prop = gen_member_expression_part(ast[2])
        # TODO check whether need to create a field
        rd = Registers.allocate(1)[0]
        builder.inst_getfield(rd, obj, prop)
        Registers.free([obj, prop])
        return rd
    elif ast[1][0] == 'AllocationExpression':
        return gen_allocation_expression(ast[1])


def gen_call_expression(ast, this=None):
    assert ast[0] == 'CallExpression'
    if ast[2][0] == 'Arguments':
        if ast[1][0] == 'MemberExpression':
            callee = gen_member_expression(ast[1])
        elif ast[1][0] == 'CallExpression':
            callee = gen_call_expression(ast[1])
        args = []
        if ast[2][-2] != '(':  # there are some arguments
            for node in ast[2][-2]:
                if type(node) == list:
                    args.append(gen_assignment_expression_no_in(node))
        temp = Registers.allocate(1)[0]
        if not this:
            builder.get_this(temp)
        else:
            temp = this
        builder.insert_comment('Prepare to call function')
        builder.call_func(callee, temp, args)
        Registers.free([callee] + args)
        builder.get_ret(temp)
        return temp
    # TODO


def gen_left_hand_side_expression(ast):
    assert ast[0] == 'LeftHandSideExpression'
    if ast[1][0] == 'MemberExpression':
        return gen_member_expression(ast[1])
    elif ast[1][0] == 'CallExpression':
        return gen_call_expression(ast[1])
    # TODO
    pass


def gen_assignment_expression_no_in(ast):
    assert ast[0] == 'AssignmentExpressionNoIn'
    if len(ast) == 2:
        if ast[1][0] == 'LeftHandSideExpression':
            return gen_left_hand_side_expression(ast[1])
        elif ast[1][0] == 'CallExpression':
            return gen_call_expression(ast[1])
        elif ast[1][0] == 'MemberExpression':
            return gen_member_expression(ast[1])
    elif len(ast) == 3:
        if ast[1][0] == 'AssignmentExpressionNoIn':
            raise Exception('Postfix operator is not supported yet.')
            rs = gen_assignment_expression_no_in(ast[1])
            rt = Registers.allocate(1)[0]
            builder.inst_la(rt, Constants.integer(1))
            if ast[2] == '++':
                builder.inst_add(rs, rs, rt)
            elif ast[2] == '--':
                builder.inst_sub(rs, rs, rt)
            Registers.free([rt])
            return rs
        elif ast[1] == '++':
            rs = gen_assignment_expression_no_in(ast[2])
            rt = Registers.allocate(1)[0]
            builder.inst_la(rt, Constants.integer(1))
            builder.inst_add(rs, rs, rt)
            Registers.free([rt])
            return rs
        elif ast[1] == '--':
            rs = gen_assignment_expression_no_in(ast[2])
            rt = Registers.allocate(1)[0]
            builder.inst_la(rt, Constants.integer(1))
            builder.inst_sub(rs, rs, rt)
            Registers.free([rt])
            return rs
        elif ast[1] == 'typeof':
            rd = Registers.allocate(1)[0]
            rs = gen_assignment_expression_no_in(ast[2])
            builder.inst_newobj(rd)
            builder.inst_typeof(rd, rs)
            Registers.free([rs])
            return rd
        elif ast[1] == '+':
            return gen_assignment_expression_no_in(ast[2])
        elif ast[1] == '-':
            rs = gen_assignment_expression_no_in(ast[2])
            rd, rt = Registers.allocate(2)
            builder.inst_la(rt, Constants.integer(-1))
            builder.inst_mul(rd, rs, rt)
            Registers.free([rs, rt])
            return rd
        elif ast[1] == '~':
            rs = gen_assignment_expression_no_in(ast[2])
            builder.inst_not(rs, rs)
            return rs
        elif ast[1] == '!':
            rs = gen_assignment_expression_no_in(ast[2])
            t1 = Registers.allocate(1)[0]
            exit_label = Labels.temp()
            true_label = Labels.temp()
            builder.inst_newobj(t1)
            builder.inst_bnz(rs, true_label)
            builder.inst_la(t1, Constants.integer(1))
            builder.inst_j(exit_label)
            builder.insert_label(true_label)
            builder.insert_la(t1, Constants.integer(0))
            builder.insert_label(exit_label)
            return t1
    elif len(ast) == 4:
        if ast[2] in ['=', '*=', '/=', '%=', '+=', '-=', '<<=', '>>=', '>>>=', '&=',
                      '^=', '|=']:
            r1 = gen_left_hand_side_expression(ast[1])
        elif ast[2] in ['||', '&&', '|', '&', '^', '==', '!=', '===', '!==',
                        '<', '>', '<=', '>=', '<<', '>>', '>>>', '+', '-', '*',
                        '/']:
            r1 = gen_assignment_expression_no_in(ast[1])
        r2 = gen_assignment_expression_no_in(ast[3])
        if ast[2] == '+':
            rd = Registers.allocate(1)[0]
            builder.inst_newobj(rd)
            builder.inst_add(rd, r1, r2)
            Registers.free([r1, r2])
            return rd
        elif ast[2] == '-':
            rd = Registers.allocate(1)[0]
            builder.inst_newobj(rd)
            builder.inst_sub(rd, r1, r2)
            Registers.free([r1, r2])
            return rd
        elif ast[2] == '*':
            rd = Registers.allocate(1)[0]
            builder.inst_newobj(rd)
            builder.inst_mul(rd, r1, r2)
            Registers.free([r1, r2])
            return rd
        elif ast[2] == '/':
            rd = Registers.allocate(1)[0]
            builder.inst_newobj(rd)
            builder.inst_div(rd, r1, r2)
            Registers.free([r1, r2])
            return rd
        elif ast[2] == '=':
            builder.inst_move(r1, r2)
            Registers.free([r2])
            return r1
        elif ast[2] == '*=':
            builder.inst_mul(r1, r1, r2)
            Registers.free([r2])
            return r1
        elif ast[2] == '/=':
            builder.inst_div(r1, r1, r2)
            Registers.free([r2])
            return r1
        elif ast[2] == '%=':
            builder.inst_mod(r1, r1, r2)
            Registers.free([r2])
            return r1
        elif ast[2] == '+=':
            builder.inst_add(r1, r1, r2)
            Registers.free([r2])
            return r1
        elif ast[2] == '-=':
            builder.inst_sub(r1, r1, r2)
            Registers.free([r2])
            return r1
        elif ast[2] == '<<=':
            builder.inst_sll(r1, r1, r2)
            Registers.free([r2])
            return r1
        elif ast[2] == '>>=':
            builder.inst_sra(r1, r1, r2)
            Registers.free([r2])
            return r1
        elif ast[2] == '>>>=':
            builder.inst_srl(r1, r1, r2)
            Registers.free([r2])
            return r1
        elif ast[2] == '&=':
            builder.inst_and(r1, r1, r2)
            Registers.free([r2])
            return r1
        elif ast[2] == '^=':
            builder.inst_xor(r1, r1, r2)
            Registers.free([r2])
            return r1
        elif ast[2] == '|=':
            builder.inst_or(r1, r1, r2)
            Registers.free([r2])
            return r1
        elif ast[2] == '||':
            rd = Registers.allocate(1)[0]
            exit_label = Labels.temp()
            ret_r1 = Labels.temp()

            builder.inst_newobj(rd)
            builder.inst_bnz(r1, ret_r1)
            builder.inst_move(rd, r2)
            builder.inst_j(exit_label)
            builder.insert_label(ret_r1)
            builder.inst_move(rd, r1)
            builder.insert_label(exit_label)

            Registers.free([r1, r2])
            return rd
        elif ast[2] == '&&':
            rd = Registers.allocate(1)[0]
            exit_label = Labels.temp()
            ret_r1 = Labels.temp()

            builder.inst_newobj(rd)
            builder.inst_bez(r1, ret_r1)
            builder.inst_move(rd, r2)
            builder.inst_j(exit_label)
            builder.insert_label(ret_r1)
            builder.inst_move(rd, r1)
            builder.insert_label(exit_label)

            Registers.free([r1, r2])
            return rd
        elif ast[2] == '|':
            rd = Registers.allocate(1)[0]
            builder.inst_newobj(rd)
            builder.inst_or(rd, r1, r2)
            Registers.free([r1, r2])
            return rd
        elif ast[2] == '&':
            rd = Registers.allocate(1)[0]
            builder.inst_newobj(rd)
            builder.inst_and(rd, r1, r2)
            Registers.free([r1, r2])
            return rd
        elif ast[2] == '^':
            rd = Registers.allocate(1)[0]
            builder.inst_newobj(rd)
            builder.inst_xor(rd, r1, r2)
            Registers.free([r1, r2])
            return rd
        elif ast[2] == '==' or ast[2] == '===':
            rd = Registers.allocate(1)[0]
            builder.inst_newobj(rd)
            builder.inst_cmp(rd, r1, r2)
            Registers.free([r1, r2])
            return rd
        elif ast[2] == '!=' or ast[2] == '!==':
            rd = Registers.allocate(1)[0]
            builder.inst_newobj(rd)
            builder.inst_cmp(rd, r1, r2)
            builder.inst_la(r1, Constants.integer(1))
            builder.inst_sub(rd, r1, rd)
            Registers.free([r1, r2])
            return rd
        elif ast[2] == '<':
            rd = Registers.allocate(1)[0]
            builder.inst_newobj(rd)
            builder.inst_slt(rd, r1, r2)
            Registers.free([r1, r2])
            return rd
        elif ast[2] == '>':
            rd = Registers.allocate(1)[0]
            builder.inst_newobj(rd)
            builder.inst_slt(rd, r2, r1)
            Registers.free([r1, r2])
            return rd
        elif ast[2] == '<=':
            rd = Registers.allocate(1)[0]
            builder.inst_newobj(rd)
            builder.inst_slt(rd, r2, r1)
            builder.inst_la(r1, Constants.integer(1))  # TODO: r1 should not be modified
            builder.inst_not(rd, r1, rd)
            Registers.free([r1, r2])
            return rd
        elif ast[2] == '>=':
            rd = Registers.allocate(1)[0]
            builder.inst_newobj(rd)
            builder.inst_slt(rd, r1, r2)
            builder.inst_la(r1, Constants.integer(1))  # TODO: r1 should not be modified
            builder.inst_sub(rd, r1, rd)
            Registers.free([r1, r2])
            return rd
        elif ast[2] == '<<':
            rd = Registers.allocate(1)[0]
            builder.inst_newobj(rd)
            builder.inst_sll(rd, r1, r2)
            Registers.free([r1, r2])
            return rd
        elif ast[2] == '>>':
            rd = Registers.allocate(1)[0]
            builder.inst_newobj(rd)
            builder.inst_sra(rd, r1, r2)
            Registers.free([r1, r2])
            return rd
        elif ast[2] == '>>>':
            rd = Registers.allocate(1)[0]
            builder.inst_newobj(rd)
            builder.inst_srl(rd, r1, r2)
            Registers.free([r1, r2])
            return rd


def gen_expression_no_in(ast):
    assert ast[0] == 'ExpressionNoIn'
    if ast[1][0] == 'ExpressionNoIn':
        return gen_expression_no_in(ast[1])
    elif ast[1][0] == 'AssignmentExpressionNoIn':
        return gen_assignment_expression_no_in(ast[1])


def gen_do_statement(ast):
    assert ast[0] == 'DoStatement'
    loop_label = Labels.temp()
    gen_statement(ast[2])
    cond = gen_expression_no_in(ast[5])
    builder.inst_bnz(cond, loop_label)
    Registers.free([cond])


def gen_while_statement(ast):
    assert ast[0] == 'WhileStatement'
    exit_label = Labels.temp()
    loop_label = Labels.temp()
    builder.insert_label(loop_label)
    cond = gen_expression_no_in(ast[3])
    builder.inst_bez(cond, exit_label)
    Registers.free([cond])
    gen_statement(ast[5])
    builder.inst_j(loop_label)
    builder.insert_label(exit_label)


def gen_origin_for_statement(ast):
    assert ast[0] == 'OriginForStatement'
    exit_label = Labels.temp()
    loop_label = Labels.temp()
    gen_expression_no_in(ast[3])
    builder.insert_label(loop_label)
    cond = gen_expression_no_in(ast[5])
    builder.inst_bez(cond, exit_label)
    Registers.free([cond])
    gen_statement(ast[9])
    gen_expression_no_in(ast[7])
    builder.inst_j(loop_label)
    builder.insert_label(exit_label)


def gen_for_each_statement(ast):
    assert ast[0] == 'ForEachStatement'


def gen_return_statement(ast):
    assert ast[0] == 'ReturnStatement'
    if len(ast) >= 3 and ast[2] != ';':  # return some expression
        ret = gen_expression_no_in(ast[2])
        builder.inst_st(ret, Registers.fp(), -12)
        Registers.free([ret])
    builder.inst_ret()

    
def gen_iteration_statement(ast):
    assert ast[0] == 'IterationStatement'
    generators = {
        'DoStatement': gen_do_statement,
        'WhileStatement': gen_while_statement,
        'OriginForStatement': gen_origin_for_statement,
        'ForEachStatement': gen_for_each_statement
    }
    if ast[1][0] in generators:
        generators[ast[1][0]](ast[1])


def gen_if_statement(ast):
    assert ast[0] == 'IfStatement'
    exp = gen_expression_no_in(ast[3])
    exit_label = Labels.temp()
    if ast[-2] == 'else':  # it has 'else' clause
        else_label = Labels.temp()
        builder.inst_bez(exp, else_label)
        gen_statement(ast[5])
        builder.inst_j(exit_label)
        builder.insert_label(else_label)
        gen_statement(ast[7])
        builder.insert_label(exit_label)
    else:  # It has no 'else' clause
        builder.inst_bez(exp, exit_label)
        gen_statement(ast[5])
        builder.insert_label(exit_label)
    Registers.free([exp])


def gen_expression_no_in_statement(ast):
    assert ast[0] == 'ExpressionNoInStatement'
    rd = gen_expression_no_in(ast[1])
    Registers.free([rd])


def gen_variable_statement(ast):
    assert ast[0] == 'VariableStatement'
    identifier = gen_identifier(ast[2])
    if len(ast) > 4:
        temp = gen_assignment_expression_no_in(ast[4])
        builder.inst_move(identifier, temp)
        Registers.free([temp])
    Registers.free([identifier])


def gen_block(ast):
    assert ast[0] == 'Block'
    if len(ast[1:]) == 3:
        gen_statement_list(ast[2])


def gen_statement(ast):
    assert ast[0] == 'Statement'
    generators = {
        'Block': gen_block,
        'VariableStatement': gen_variable_statement,
        'ExpressionNoInStatement': gen_expression_no_in_statement,
        'IfStatement': gen_if_statement,
        'IterationStatement': gen_iteration_statement,
        'ReturnStatement': gen_return_statement
    }
    if ast[1][0] in generators:
        generators[ast[1][0]](ast[1])


def gen_statement_list(ast):
    assert ast[0] == 'StatementList'
    for node in ast[1:]:
        gen_statement(node)


def gen_program(ast):
    assert ast[0] == 'Program'
    gen_statement_list(ast[1])


def generate(ast):
    gen_program(ast)
    # pprint.pprint(ast)
    builder.halt()
    return builder.dump() + Constants.dump()
