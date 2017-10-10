"""
Optimizer module for Lift JS.
"""
from __future__ import print_function
import copy

def fold_constant(ast):
    # TODO
    return ast


def eliminate_unreachable(ast):
    # TODO
    return ast


def optimize(ast):
    optimize_program(ast)
    return ast


def printAST(p, n=0):
    if p is not None:
        print('  ' * n, end='')
        if type(p) is list:
            print(p[0])
            for node in p[1:]:
                printAST(node, n + 1)
        else:
            print(p)


def optimize_string_literal(string):
    return


def optimize_literal(ast):
    assert ast[0] == 'Literal'
    if type(ast[1]) == int:
        return
    elif type(ast[1]) == str:
        return
    elif type(ast[1]) == bool:
        return


def optimize_identifier(ast):
    assert ast[0] == 'Identifier'
    return


def optimize_function_body(ast):
    assert ast[0] == 'FunctionBody'
    if ast[2] != '}':
        optimize_statement_list(ast[2])


def optimize_function_expression(ast):
    assert ast[0] == 'FunctionExpression'
    if ast[2] != '(':
        optimize_identifier(ast[2])
    if ast[-3] != '(':
        # The function has arguments
        for node in ast[-3]:
            if type(node) == list:
                optimize_identifier(node)
    optimize_function_body(ast[-1])
    return


def optimize_property_name(ast):
    assert ast[0] == 'PropertyName', str(ast)
    if type(ast[1]) == list:  # identifier
        return optimize_identifier(ast[1])
    elif type(ast[1]) == str:  # string literal
        return optimize_string_literal(ast[1])
        # TODO: more type of property


def optimize_object_literal(ast):
    assert ast[0] == 'ObjectLiteral', str(ast)
    for node in ast[2]:
        if type(node) != list:
            continue
        optimize_property_name(node[1])
        node[3] = optimize_assignment_expression_no_in(node[3])
    return


def optimize_primary_expression(ast):
    ast = copy.deepcopy(ast)
    assert ast[0] == 'PrimaryExpression'
    if ast[1] == 'this':
        return ast
    elif ast[1][0] == 'Literal':
        optimize_literal(ast[1])
    elif ast[1][0] == 'Identifier':
        optimize_identifier(ast[1])
    elif ast[1][0] == 'FunctionExpression':
        optimize_function_expression(ast[1])
    elif ast[1][0] == 'ObjectLiteral':
        optimize_object_literal(ast[1])
    elif ast[1][0] == '(':
        if ast[2][0] == 'ExpressionNoIn':
            ast[2] = optimize_expression_no_in(ast[2])
        if ast[3][0] == ')':
            ast = [ast[0], ast[2][1][1][1][1][1]]
    return ast


def optimize_allocation_expression(ast):
    assert ast[0] == 'AllocationExpression'
    optimize_member_expression(ast[2])  # it should be a function

    if ast[3][-2] != '(':  # there are some arguments
        for node in ast[3][-2]:
            if type(node) == list:
                node = optimize_assignment_expression_no_in(node)
    return


def optimize_member_expression_part(ast):
    assert ast[0] == 'MemberExpressionPart'
    if ast[1] == '[':
        return optimize_expression_no_in(ast[2])
    elif ast[1] == '.':
        return optimize_identifier(ast[2])


def optimize_member_expression(ast):
    assert ast[0] == 'MemberExpression'
    if ast[1][0] == 'PrimaryExpression':
        ast[1] = optimize_primary_expression(ast[1])
    elif ast[1][0] == 'MemberExpression':
        optimize_member_expression(ast[1])
        optimize_member_expression_part(ast[2])
        # TODO check whether need to create a field
    elif ast[1][0] == 'AllocationExpression':
        optimize_allocation_expression(ast[1])
    return


def optimize_argument_list(ast):
    assert ast[0] == 'ArgumentList'
    for index, node in enumerate(ast[1]):
        if type(node) == list:
            if node[0] == 'AssignmentExpressionNoIn':
                ast[1][index] = optimize_assignment_expression_no_in(node)


def optimize_call_expression(ast, this=None):
    assert ast[0] == 'CallExpression'
    if ast[2][0] == 'Arguments':
        if ast[1][0] == 'MemberExpression':
            optimize_member_expression(ast[1])
        elif ast[1][0] == 'CallExpression':
            optimize_call_expression(ast[1])
        if ast[2][-2] != '(':  # there are some arguments
            optimize_argument_list(ast[2][-2])
        return
        # TODO


def optimize_left_hand_side_expression(ast):

    assert ast[0] == 'LeftHandSideExpression'
    if ast[1][0] == 'MemberExpression':
        optimize_member_expression(ast[1])
    elif ast[1][0] == 'CallExpression':
        optimize_call_expression(ast[1])
    return


def optimize_assignment_expression_no_in(ast):
    ast = copy.deepcopy(ast)
    assert ast[0] == 'AssignmentExpressionNoIn'
    if len(ast) == 2:
        if ast[1][0] == 'LeftHandSideExpression':
            optimize_left_hand_side_expression(ast[1])
        elif ast[1][0] == 'CallExpression':
            optimize_call_expression(ast[1])
        elif ast[1][0] == 'MemberExpression':
            optimize_member_expression(ast[1])
    elif len(ast) == 3:
        if ast[1][0] == 'AssignmentExpressionNoIn':
            raise Exception('Postfix operator is not supported yet.')
        elif ast[1] == '++':
            ast[2] = optimize_assignment_expression_no_in(ast[2])
        elif ast[1] == '--':
            ast[2] = optimize_assignment_expression_no_in(ast[2])
        elif ast[1] == 'typeof':
            ast[2] = optimize_assignment_expression_no_in(ast[2])
        elif ast[1] == '+':
            ast[2] = optimize_assignment_expression_no_in(ast[2])
        elif ast[1] == '-':
            ast[2] = optimize_assignment_expression_no_in(ast[2])
        elif ast[1] == '~':
            ast[2] = optimize_assignment_expression_no_in(ast[2])
        elif ast[1] == '!':
            ast[2] = optimize_assignment_expression_no_in(ast[2])
    elif len(ast) == 4:
        if ast[2] in ['=', '*=', '/=', '%=', '+=', '-=', '<<=', '>>=', '>>>=', '&=',
                      '^=', '|=']:
            optimize_left_hand_side_expression(ast[1])
            ast[3] = optimize_assignment_expression_no_in(ast[3])
        elif ast[2] in ['||', '&&', '|', '&', '^', '==', '!=', '===', '!==',
                        '<', '>', '<=', '>=', '<<', '>>', '>>>', '+', '-', '*',
                        '/']:
            ast[1] = optimize_assignment_expression_no_in(ast[1])
            ast[3] = optimize_assignment_expression_no_in(ast[3])
            if(ast[1][1][1][1][1][0] == 'Literal' and ast[3][1][1][1][1][0] == 'Literal'):
                operand1 = ast[1][1][1][1][1][1]
                operand2 = ast[3][1][1][1][1][1]
            else:
                return ast

        if ast[2] == '+':
            ast = ast[1]
            ast[1][1][1][1][1] = operand1 + operand2
        elif ast[2] == '-':
            ast = ast[1]
            ast[1][1][1][1][1] = operand1 - operand2
        elif ast[2] == '*':
            ast = ast[1]
            ast[1][1][1][1][1] = operand1 * operand2
        elif ast[2] == '/':
            ast = ast[1]
            ast[1][1][1][1][1] = operand1 / operand2
        elif ast[2] == '=':
            pass
        elif ast[2] == '*=':
            pass
        elif ast[2] == '/=':
            pass
        elif ast[2] == '%=':
            pass
        elif ast[2] == '+=':
            pass
        elif ast[2] == '-=':
            pass
        elif ast[2] == '<<=':
            pass
        elif ast[2] == '>>=':
            pass
        elif ast[2] == '>>>=':
            pass
        elif ast[2] == '&=':
            pass
        elif ast[2] == '^=':
            pass
        elif ast[2] == '|=':
            pass
        elif ast[2] == '||':
            ast = ast[1]
            ast[1][1][1][1][1] = operand1 or operand2
        elif ast[2] == '&&':
            ast = ast[1]
            ast[1][1][1][1][1] = operand1 and operand2
        elif ast[2] == '|':
            ast = ast[1]
            ast[1][1][1][1][1] = operand1 | operand2
        elif ast[2] == '&':
            ast = ast[1]
            ast[1][1][1][1][1] = operand1 & operand2
        elif ast[2] == '^':
            ast = ast[1]
            ast[1][1][1][1][1] = operand1 ^ operand2
        elif ast[2] == '==' or ast[2] == '===':
            ast = ast[1]
            ast[1][1][1][1][1] = operand1 == operand2
        elif ast[2] == '!=' or ast[2] == '!==':
            ast = ast[1]
            ast[1][1][1][1][1] = operand1 != operand2
        elif ast[2] == '<':
            ast = ast[1]
            ast[1][1][1][1][1] = operand1 < operand2
        elif ast[2] == '>':
            ast = ast[1]
            ast[1][1][1][1][1] = operand1 > operand2
        elif ast[2] == '<=':
            ast = ast[1]
            ast[1][1][1][1][1] = operand1 <= operand2
        elif ast[2] == '>=':
            ast = ast[1]
            ast[1][1][1][1][1] = operand1 >= operand2
        elif ast[2] == '<<':
            ast = ast[1]
            ast[1][1][1][1][1] = operand1 << operand2
        elif ast[2] == '>>':
            ast = ast[1]
            ast[1][1][1][1][1] = operand1 >> operand2
        elif ast[2] == '>>>':
            pass
    return ast


def optimize_expression_no_in(ast):
    ast = copy.deepcopy(ast)
    assert ast[0] == 'ExpressionNoIn'
    if ast[1][0] == 'ExpressionNoIn':
        ast[1] = optimize_expression_no_in(ast[1])
    elif ast[1][0] == 'AssignmentExpressionNoIn':
        ast[1] = optimize_assignment_expression_no_in(ast[1])
    return ast


def optimize_do_statement(ast):
    assert ast[0] == 'DoStatement'
    optimize_statement(ast[2])
    ast[5] = optimize_expression_no_in(ast[5])


def optimize_while_statement(ast):
    assert ast[0] == 'WhileStatement'
    ast[3] = optimize_expression_no_in(ast[3])


def optimize_origin_for_statement(ast):
    assert ast[0] == 'OriginForStatement'
    ast[3] = optimize_expression_no_in(ast[3])
    ast[5] = optimize_expression_no_in(ast[5])
    optimize_statement(ast[9])
    ast[7] = optimize_expression_no_in(ast[7])


def optimize_for_each_statement(ast):
    assert ast[0] == 'ForEachStatement'


def optimize_return_statement(ast):
    assert ast[0] == 'ReturnStatement'
    if len(ast) >= 3 and ast[2] != ';':  # return some expression
        ast[2] = optimize_expression_no_in(ast[2])


def optimize_iteration_statement(ast):
    assert ast[0] == 'IterationStatement'
    optimizers = {
        'DoStatement': optimize_do_statement,
        'WhileStatement': optimize_while_statement,
        'OriginForStatement': optimize_origin_for_statement,
        'ForEachStatement': optimize_for_each_statement
    }
    if ast[1][0] in optimizers:
        optimizers[ast[1][0]](ast[1])


def optimize_if_statement(ast):
    assert ast[0] == 'IfStatement'
    ast[3] = optimize_expression_no_in(ast[3])
    if ast[-2] == 'else':  # it has 'else' clause
        optimize_statement(ast[5])
        optimize_statement(ast[7])
    else:  # It has no 'else' clause
        optimize_statement(ast[5])


def optimize_expression_no_in_statement(ast):
    assert ast[0] == 'ExpressionNoInStatement'
    ast[1] = optimize_expression_no_in(ast[1])


def optimize_variable_statement(ast):
    assert ast[0] == 'VariableStatement'
    optimize_identifier(ast[2])
    if len(ast) > 4:
        ast[4] = optimize_assignment_expression_no_in(ast[4])


def optimize_block(ast):
    assert ast[0] == 'Block'
    if len(ast[1:]) == 3:
        optimize_statement_list(ast[2])


def optimize_statement(ast):
    ast = copy.deepcopy(ast)
    assert ast[0] == 'Statement'
    optimizers = {
        'Block': optimize_block,
        'VariableStatement': optimize_variable_statement,
        'ExpressionNoInStatement': optimize_expression_no_in_statement,
        'IfStatement': optimize_if_statement,
        'IterationStatement': optimize_iteration_statement,
        'ReturnStatement': optimize_return_statement
    }
    if ast[1][0] in optimizers:
        optimizers[ast[1][0]](ast[1])
    if ast[1][0] == 'IfStatement':
        ast = eliminate_unreachable_if_statement(ast)
    elif ast[1][0] == 'IterationStatement':
        if ast[1][1][0] == 'WhileStatement':
            ast = eliminate_unreachable_while_statement(ast)
    return ast


def optimize_statement_list(ast):
    assert ast[0] == 'StatementList'
    for i in range(1, len(ast)):
        ast[i] = optimize_statement(ast[i])


def optimize_program(ast):
    assert ast[0] == 'Program'
    optimize_statement_list(ast[1])


def eliminate_unreachable_if_statement(ast):
    ast = copy.deepcopy(ast)
    assert ast[0] == 'Statement'
    if_ast = ast[1]
    assert if_ast[0] =='IfStatement'
    if len(if_ast) == 8:  # if with else
        if if_ast[3][1][1][1][1][1][0] == 'Literal':  # constant
            if if_ast[3][1][1][1][1][1][1]:  # eliminate statements in else
                ast = ast[1][5]
            else:  # eliminate statements in if
                ast = ast[1][7]
    else:  # if without else
        if if_ast[3][1][1][1][1][1][0] == 'Literal':  # constant
            if not if_ast[3][1][1][1][1][1][1]:  # eliminate these statements
                empty_ast = ['EmptyStatement', ';']
                ast[1] = empty_ast
            else:  # eliminate judge statements
                ast = ast[1][5]
    return ast
    

def eliminate_unreachable_while_statement(ast):
    ast = copy.deepcopy(ast)
    assert ast[0] == 'Statement'
    while_ast = ast[1][1]
    assert while_ast[0] =='WhileStatement'
    if while_ast[3][1][1][1][1][1][0] == 'Literal':  # constant
        if not while_ast[3][1][1][1][1][1][1]:  # eliminate these statements
            empty_ast = ['EmptyStatement', ';']
            ast[1] = empty_ast
    return ast
