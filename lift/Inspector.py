"""
Syntax Inspector for Lift JS.
"""
import Parser
import Inspector

scope_list = []
correct = True


def inspect_string_literal(string):
    return


def inspect_literal(ast):
    assert ast[0] == 'Literal'
    if type(ast[1]) == int:
        return
    elif type(ast[1]) == str:
        return
    elif type(ast[1]) == bool:
        return


def inspect_identifier(ast):
    assert ast[0] == 'Identifier'
    ast[1].type = 'Identifier'
    return ast[1]


def check_identifier(i):
    undelcared = True
    if isinstance(i, Parser.LiftStr) and i.type == 'Identifier':
        for scope in scope_list:
            if i in scope:
                undelcared = False
                break
        if undelcared:
            Inspector.correct = False
            err_msg = "line %d, column %d: undelcared object %s\n" % (i.position[0], i.position[1], i);
            err_msg += Parser.print_error(Parser.lexer, i.position[0], i.pos)
            Parser.error_list[i.pos] = err_msg
    pass


def inspect_function_body(ast):
    assert ast[0] == 'FunctionBody'
    try:
        if ast[2] != '}':
            inspect_statement_list(ast[2])
    except:
        pass


def inspect_function_expression(ast):
    assert ast[0] == 'FunctionExpression'
    scope_list.append([])
    try:
        if ast[2] != '(':
            scope_list[-1].append(inspect_identifier(ast[2]))
        if ast[-3] != '(':
            # The function has arguments
            for node in ast[-3]:
                if type(node) == list:
                    scope_list[-1].append(inspect_identifier(node))
    except:
        pass
    try:
        inspect_function_body(ast[-1])
    except:
        pass
    scope_list.pop()
    return


def inspect_property_name(ast):
    assert ast[0] == 'PropertyName', str(ast)
    try:
        if type(ast[1]) == list:  # identifier
            return inspect_identifier(ast[1])
        elif type(ast[1]) == str:  # string literal
            return inspect_string_literal(ast[1])
    except:
        pass
        # TODO: more type of property


def inspect_object_literal(ast):
    assert ast[0] == 'ObjectLiteral', str(ast)
    for node in ast[2]:
        if type(node) != list:
            continue
        try:
            inspect_property_name(node[1])
            inspect_assignment_expression_no_in(node[3])
        except:
            pass
    return


def inspect_primary_expression(ast):
    assert ast[0] == 'PrimaryExpression'
    try:
        if ast[1] == 'this':
            return
        elif ast[1][0] == 'Literal':
            return inspect_literal(ast[1])
        elif ast[1][0] == 'Identifier':
            return inspect_identifier(ast[1])
        elif ast[1][0] == 'FunctionExpression':
            return inspect_function_expression(ast[1])
        elif ast[1][0] == 'ObjectLiteral':
            return inspect_object_literal(ast[1])
    except:
        pass
    # TODO
    pass


def inspect_allocation_expression(ast):
    assert ast[0] == 'AllocationExpression'
    try:
        inspect_member_expression(ast[2])  # it should be a function
    except:
        pass
    try:
        if ast[3][-2] != '(':  # there are some arguments
            for node in ast[3][-2]:
                if type(node) == list:
                    inspect_assignment_expression_no_in(node)
    except:
        pass
    return


def inspect_member_expression_part(ast):
    assert ast[0] == 'MemberExpressionPart'
    try:
        if ast[1] == '[':
            return inspect_expression_no_in(ast[2])
        elif ast[1] == '.':
            return inspect_identifier(ast[2])
    except:
        pass


def inspect_member_expression(ast):
    assert ast[0] == 'MemberExpression'
    try:
        if ast[1][0] == 'PrimaryExpression':
            return inspect_primary_expression(ast[1])
        elif ast[1][0] == 'MemberExpression':
            inspect_member_expression(ast[1])
            inspect_member_expression_part(ast[2])
            # TODO check whether need to create a field
            return
        elif ast[1][0] == 'AllocationExpression':
            return inspect_allocation_expression(ast[1])
    except:
        pass


def inspect_call_expression(ast, this=None):
    assert ast[0] == 'CallExpression'
    try:
        if ast[2][0] == 'Arguments':
            if ast[1][0] == 'MemberExpression':
                inspect_member_expression(ast[1])
            elif ast[1][0] == 'CallExpression':
                inspect_call_expression(ast[1])
            if ast[2][-2] != '(':  # there are some arguments
                for node in ast[2][-2]:
                    try:
                        if type(node) == list:
                            inspect_assignment_expression_no_in(node)
                    except:
                        pass
            return
    except:
        pass
        # TODO


def inspect_left_hand_side_expression(ast):
    assert ast[0] == 'LeftHandSideExpression'
    try:
        if ast[1][0] == 'MemberExpression':
            return inspect_member_expression(ast[1])
        elif ast[1][0] == 'CallExpression':
            return inspect_call_expression(ast[1])
    except:
        pass
    # TODO
    pass


def inspect_assignment_expression_no_in(ast):
    assert ast[0] == 'AssignmentExpressionNoIn'
    if len(ast) == 2:
        try:
            if ast[1][0] == 'LeftHandSideExpression':
                return inspect_left_hand_side_expression(ast[1])
            elif ast[1][0] == 'CallExpression':
                return inspect_call_expression(ast[1])
            elif ast[1][0] == 'MemberExpression':
                return inspect_member_expression(ast[1])
        except:
            pass
    elif len(ast) == 3:
        try:
            if ast[1][0] == 'AssignmentExpressionNoIn':
                raise Exception('Postfix operator is not supported yet.')
            elif ast[1] == '++':
                inspect_assignment_expression_no_in(ast[2])
                return
            elif ast[1] == '--':
                inspect_assignment_expression_no_in(ast[2])
                return
            elif ast[1] == 'typeof':
                inspect_assignment_expression_no_in(ast[2])
                return
            elif ast[1] == '+':
                return inspect_assignment_expression_no_in(ast[2])
            elif ast[1] == '-':
                inspect_assignment_expression_no_in(ast[2])
                return
            elif ast[1] == '~':
                inspect_assignment_expression_no_in(ast[2])
                return
            elif ast[1] == '!':
                inspect_assignment_expression_no_in(ast[2])
                return
        except:
            pass
    elif len(ast) == 4:
        try:
            if ast[2] in ['=', '*=', '/=', '%=', '+=', '-=', '<<=', '>>=', '>>>=', '&=',
                          '^=', '|=']:
                inspect_left_hand_side_expression(ast[1])
            elif ast[2] in ['||', '&&', '|', '&', '^', '==', '!=', '===', '!==',
                            '<', '>', '<=', '>=', '<<', '>>', '>>>', '+', '-', '*',
                            '/']:
                check_identifier(inspect_assignment_expression_no_in(ast[1]))
        except:
            pass
        try:
            check_identifier(inspect_assignment_expression_no_in(ast[3]))
        except:
            pass
        try:
            if ast[2] == '+':
                return
            elif ast[2] == '-':
                return
            elif ast[2] == '*':
                return
            elif ast[2] == '/':
                return
            elif ast[2] == '=':
                return
            elif ast[2] == '*=':
                return
            elif ast[2] == '/=':
                return
            elif ast[2] == '%=':
                return
            elif ast[2] == '+=':
                return
            elif ast[2] == '-=':
                return
            elif ast[2] == '<<=':
                return
            elif ast[2] == '>>=':
                return
            elif ast[2] == '>>>=':
                return
            elif ast[2] == '&=':
                return
            elif ast[2] == '^=':
                return
            elif ast[2] == '|=':
                return
            elif ast[2] == '||':
                return
            elif ast[2] == '&&':
                return
            elif ast[2] == '|':
                return
            elif ast[2] == '&':
                return
            elif ast[2] == '^':
                return
            elif ast[2] == '==' or ast[2] == '===':
                return
            elif ast[2] == '!=' or ast[2] == '!==':
                return
            elif ast[2] == '<':
                return
            elif ast[2] == '>':
                return
            elif ast[2] == '<=':
                return
            elif ast[2] == '>=':
                return
            elif ast[2] == '<<':
                return
            elif ast[2] == '>>':
                return
            elif ast[2] == '>>>':
                return
        except:
            pass


def inspect_expression_no_in(ast):
    assert ast[0] == 'ExpressionNoIn'
    try:
        if ast[1][0] == 'ExpressionNoIn':
            return inspect_expression_no_in(ast[1])
        elif ast[1][0] == 'AssignmentExpressionNoIn':
            return inspect_assignment_expression_no_in(ast[1])
    except:
        pass


def inspect_do_statement(ast):
    assert ast[0] == 'DoStatement'
    try:
        inspect_statement(ast[2])
    except:
        pass
    try:
        inspect_expression_no_in(ast[5])
    except:
        pass


def inspect_while_statement(ast):
    assert ast[0] == 'WhileStatement'
    try:
        inspect_expression_no_in(ast[3])
    except:
        pass


def inspect_origin_for_statement(ast):
    assert ast[0] == 'OriginForStatement'
    inspectors = {
        'ExpressionNoIn': inspect_expression_no_in,
        'Statement': inspect_statement,
    }

    for item in ast[1:]:
        try:
            if item[0] in inspectors:
                inspectors[item[0]](item)
        except:
            pass


def inspect_for_each_statement(ast):
    assert ast[0] == 'ForEachStatement'


def inspect_return_statement(ast):
    assert ast[0] == 'ReturnStatement'
    try:
        if len(ast) >= 3 and ast[2] != ';':  # return some expression
            inspect_expression_no_in(ast[2])
    except:
        pass


def inspect_iteration_statement(ast):
    assert ast[0] == 'IterationStatement'
    inspectors = {
        'DoStatement': inspect_do_statement,
        'WhileStatement': inspect_while_statement,
        'OriginForStatement': inspect_origin_for_statement,
        'ForEachStatement': inspect_for_each_statement
    }
    try:
        if ast[1][0] in inspectors:
            inspectors[ast[1][0]](ast[1])
    except:
        pass


def inspect_if_statement(ast):
    assert ast[0] == 'IfStatement'
    try:
        inspect_expression_no_in(ast[3])
    except:
        pass
    if ast[-2] == 'else':  # it has 'else' clause
        try:
            inspect_statement(ast[5])
        except:
            pass
        try:
            inspect_statement(ast[7])
        except:
            pass
    else:  # It has no 'else' clause
        try:
            inspect_statement(ast[5])
        except:
            pass


def inspect_expression_no_in_statement(ast):
    assert ast[0] == 'ExpressionNoInStatement'
    try:
        inspect_expression_no_in(ast[1])
    except:
        pass


def inspect_variable_statement(ast):
    assert ast[0] == 'VariableStatement'
    try:
        scope_list[-1].append(inspect_identifier(ast[2]))
    except:
        pass
    try:
        if len(ast) > 4:
            inspect_assignment_expression_no_in(ast[4])
    except:
        pass


def inspect_block(ast):
    assert ast[0] == 'Block'
    try:
        if len(ast[1:]) == 3:
            inspect_statement_list(ast[2])
    except:
        pass


def inspect_statement(ast):
    assert ast[0] == 'Statement'
    inspectors = {
        'Block': inspect_block,
        'VariableStatement': inspect_variable_statement,
        'ExpressionNoInStatement': inspect_expression_no_in_statement,
        'IfStatement': inspect_if_statement,
        'IterationStatement': inspect_iteration_statement,
        'ReturnStatement': inspect_return_statement
    }
    try:
        if ast[1][0] in inspectors:
            inspectors[ast[1][0]](ast[1])
    except:
        pass


def inspect_statement_list(ast):
    assert ast[0] == 'StatementList'

    for node in ast[1:]:
        try:
            inspect_statement(node)
        except:
            pass


def inspect_program(ast):
    assert ast[0] == 'Program'
    try:
        scope_list.append([])
        inspect_statement_list(ast[1])
        scope_list.pop()
    except:
        pass


def inspect(ast):
    try:
        # print(ast)
        # Parser.printAST(ast)
        inspect_program(ast)
    except:
        pass
    return Inspector.correct
