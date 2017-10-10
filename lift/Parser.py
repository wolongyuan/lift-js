from __future__ import print_function
import ply.lex as lex
import ply.yacc as yacc
import Inspector
import Parser

import sys

correct = True
error_list = {}
# import pdb
unsupported = (
    'abstract',
    'arguments',
    'boolean',
    'byte',
    'case',
    'catch',
    'char',
    'class',
    'const',
    'debugger',
    'default',
    'delete',
    'double',
    'enum',
    'eval',
    'export',
    'extends',
    'false',
    'final',
    'finally',
    'float',
    'goto',
    'implements',
    'import',
    'instanceof',
    'int',
    'interface',
    'let',
    'long',
    'native',
    'package',
    'private',
    'protected',
    'public',
    'short',
    'static',
    'super',
    'switch',
    'synchronized',
    'throw',
    'throws',
    'transient',
    'true',
    'try',
    'volatile',
    'with',
    'yield'
)
reserved = {
    #     'abstract':'ABSTRACT',
    #     'arguments':'ARGUMENTS',
    #     'boolean':'BOOLEAN',
    #     'break':'BREAK',
    #     'byte':'BYTE',
    #     'case':'CASE',
    #     'catch':'CATCH',
    #     'char':'CHAR',
    #     'class':'CLASS',
    #     'const':'CONST',
    #     'continue':'CONTINUE',
    #     'debugger':'DEBUGGER',
    #     'default':'DEFAULT',
    # 'delete': 'DELETE',
    'do': 'DO',
    # 'double':'DOUBLE',
    'else': 'ELSE',
    # 'enum':'ENUM',
    # 'eval':'EVAL',
    # 'export':'EXPORT',
    # 'extends':'EXTENDS',
    # 'false':'FALSE',
    # 'final':'FINAL',
    # 'finally':'FINALLY',
    # 'float':'FLOAT',
    'for': 'FOR',
    'function': 'FUNCTION',
    # 'goto':'GOTO',
    'if': 'IF',
    # 'implements':'IMPLEMENTS',
    # 'import':'IMPORT',
    'in': 'IN',
    # 'instanceof': 'INSTANCEOF',
    # 'int':'INT',
    # 'interface':'INTERFACE',
    # 'let':'LET',
    # 'long':'LONG',
    # 'native':'NATIVE',
    'new': 'NEW',
    'null': 'NULL',
    # 'package':'PACKAGE',
    'print': 'PRINT',
    # 'private':'PRIVATE',
    # 'protected':'PROTECTED',
    # 'public':'PUBLIC',
    'return': 'RETURN',
    # 'short':'SHORT',
    # 'static':'STATIC',
    # 'super':'SUPER',
    # 'switch':'SWITCH',
    # 'synchronized':'SYNCHRONIZED',
    'this': 'THIS',
    # 'throw':'THROW',
    # 'throws':'THROWS',
    # 'transient':'TRANSIENT',
    # 'true':'TRUE',
    # 'try':'TRY',
    'typeof': 'TYPEOF',
    'var': 'VAR',
    'void': 'VOID',
    # 'volatile':'VOLATILE',
    'while': 'WHILE',
    # 'with':'WITH',
    # 'yield':'YIELD'
}

operator = [
    "PLUS_PLUS",
    "MINUS_MINUS",
    "PLUS",
    "MINUS",
    "BIT_WISE_NOT",
    "NOT",
    "EQUAL_EQUAL",
    "NOT_EQUAL",
    "EQUAL_EQUAL_EQUAL",
    "NOT_EQUAL_EQUAL",
    "EQUAL",
    "MUL_EQUAL",
    "DIV_EQUAL",
    "MOD_EQUAL",
    "PLUS_EQUAL",
    "MINUS_EQUAL",
    "SHIFT_LEFT_EQUAL",
    "SHIFT_RIGHT_ARITHMATIC_EQUAL",
    "SHIFT_RIGHT_LOGIC_EQUAL",
    "AND_EQUAL",
    "XOR_EQUAL",
    "OR_EQUAL",
    "SHIFT_LEFT",
    "SHIFT_RIGHT_ARITHMATIC",
    "SHIFT_RIGHT_LOGIC",
    "AND_AND",
    "OR_OR",
    "LESS_THAN",
    "GREAT_THAN",
    "LESS_EQUAL_THAN",
    "GREAT_EQUAL_THAN",
    "MUL",
    "DIV",
    "MOD",
    "OR",
    "XOR",
    "AND"
]

tokens = [
             'IDENTIFIER_NAME',
             'FLOAT_LITERAL',
             'DECIMAL_INTEGER_LITERAL',
             'HEX_INTEGER_LITERAL',
             'BOOLEAN_LITERAL',
             'STRING_LITERAL',
         ] + list(reserved.values()) + operator


def t_BOOLEAN_LITERAL(t):
    r'false|true'
    if t.value == "true":
        t.value = True
    elif t.value == "false":
        t.value = False
    t.value = bool(t.value)
    return t


class LiftStr(str):
    def __new__(cls, value, *args, **keywargs):
        return str.__new__(cls, value)

    def __init__(self, value, position):
        super(LiftStr, self).__init__(value)
        self.position = position


def t_IDENTIFIER_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in unsupported:
        raise Exception('"' + t.value + '" is Forbidden used as Identifier.')
    t.type = reserved.get(t.value, 'IDENTIFIER_NAME')  # Check for reserved words
    i = t.lexer.lines[t.lexer.lineno - 1]
    t.value = LiftStr(t.value, (t.lexer.lineno, t.lexer.lexpos - i))
    t.value.pos = t.lexer.lexpos
    return t


t_PLUS_PLUS = r"\+\+"
t_MINUS_MINUS = r"--"
t_PLUS = r"\+"
t_MINUS = r"-"
t_BIT_WISE_NOT = r"~"
t_NOT = r"!"
t_EQUAL_EQUAL = r"=="
t_NOT_EQUAL = r"!="
t_EQUAL_EQUAL_EQUAL = r"==="
t_NOT_EQUAL_EQUAL = r"!=="
t_EQUAL = r"="
t_MUL_EQUAL = r"\*="
t_DIV_EQUAL = r"/="
t_MOD_EQUAL = r"%="
t_PLUS_EQUAL = r"\+="
t_MINUS_EQUAL = r"-="
t_SHIFT_LEFT_EQUAL = r"<<="
t_SHIFT_RIGHT_ARITHMATIC_EQUAL = r">>="
t_SHIFT_RIGHT_LOGIC_EQUAL = r">>>="
t_AND_EQUAL = r"&="
t_XOR_EQUAL = r"^="
t_OR_EQUAL = r"\|="
t_SHIFT_LEFT = r"<<"
t_SHIFT_RIGHT_ARITHMATIC = r">>"
t_SHIFT_RIGHT_LOGIC = r">>>"
t_AND_AND = r"&&"
t_OR_OR = r"\|\|"
t_LESS_THAN = r"<"
t_GREAT_THAN = r">"
t_LESS_EQUAL_THAN = r"<="
t_GREAT_EQUAL_THAN = r">="
t_MUL = r"\*"
t_DIV = r"/"
t_MOD = r"%"
t_OR = r"\|"
t_XOR = r"\^"
t_AND = r"&"

precedence = (
    ('left', 'MUL_EQUAL', 'DIV_EQUAL', 'MOD_EQUAL', 'PLUS_EQUAL', 'MINUS_EQUAL', 'SHIFT_LEFT_EQUAL',
     'SHIFT_RIGHT_ARITHMATIC_EQUAL', 'SHIFT_RIGHT_LOGIC_EQUAL', 'AND_EQUAL', 'XOR_EQUAL', 'OR_EQUAL'),
    ('left', 'OR_OR'),
    ('left', 'AND_AND'),
    ('left', 'OR'),
    ('left', 'XOR'),
    ('left', 'AND'),
    ('right', 'EQUAL_EQUAL', 'NOT_EQUAL', 'EQUAL_EQUAL_EQUAL', 'NOT_EQUAL_EQUAL'),
    ('nonassoc', 'LESS_THAN', 'GREAT_THAN', 'LESS_EQUAL_THAN', 'GREAT_EQUAL_THAN'),
    ('left', 'SHIFT_LEFT', 'SHIFT_RIGHT_ARITHMATIC', 'SHIFT_RIGHT_LOGIC'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV', 'MOD'),
    ('right', 'NOT'),
    ('nonassoc', 'UNARY'),
    ('nonassoc', 'RIGHT_HAND'),
    ('nonassoc', 'LEFT_HAND')
)


# pdb.set_trace()

def t_STRING_LITERAL(t):
    r'("([^\\"]|\\"|\\\\|\\n|\\t|\\r|\\v|\\b|\\f)*")|(\'([^\\\']|\\\'|\\\\|\\n|\\t|\\r|\\v|\\b|\\f)*\')'
    t.value = eval(t.value)
    return t


def t_COMMENT(t):
    r'(//.*)|(/\*(.|\n)*\*/)'
    length = t.value.count("\n")
    t.lexer.lineno += length
    for i in range(0, length):
        t.lexer.lines.append(t.lexer.lexpos)
    pass
    # No return value. Token discarded


def t_FLOAT_LITERAL(t):
    r'(\d+\.\d+)|(\d+e-?\d+)'
    t.value = float(t.value)
    return t


def t_DECIMAL_INTEGER_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_HEX_INTEGER_LITERAL(t):
    r'0x\d+'
    t.value = int(t.value)
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    length = len(t.value)
    t.lexer.lineno += length
    for i in range(0, length):
        t.lexer.lines.append(t.lexer.lexpos)


# Error handling rule
def t_error(t):
    Parser.correct = False
    i = t.lexer.lines[t.lexer.lineno - 1]
    err_msg = "line %d, column %d: Illegal character '%s'\n" % (t.lexer.lineno, t.lexer.lexpos - i, t.value[0])
    t.lexer.skip(1)
    err_msg += print_error(t.lexer, t.lexer.lineno, t.lexer.lexpos)
    error_list[t.lexer.lexpos] = err_msg


t_ignore = ' \t\f\v'
literals = "(){}[];.,?:"


def p_error(t):
    Parser.correct = False
    # if t is None:
    #     return
    i = t.lexer.lines[t.lexer.lineno - 1]
    err_msg = "line %d, column %d: unexpected token %s\n" % (t.lexer.lineno, t.lexer.lexpos - i, t.value)
    err_msg += print_error(t.lexer, t.lexer.lineno, t.lexer.lexpos)
    error_list[t.lexer.lexpos] = err_msg


def print_error(l, line_num, pos):
    data_len = len(l.lexdata)
    data = l.lexdata
    i = l.lines[line_num - 1]
    ret = ""
    while i < data_len and data[i] != "\n":
        ret += data[i]
        i += 1
    ret += "\n"
    i = l.lines[line_num - 1]
    while i < data_len and data[i] != "\n":
        i += 1
        ret += "^" if i == pos else " "
    ret += "\n"
    return ret


def p_Block(p):
    """Block : '{' StatementList '}'
    | '{'  '}' """
    p[0] = "Block"
    p[0] = list(p)
    # print("Block")


def p_PrimaryExpression(p):
    """PrimaryExpression : THIS
    |   ObjectLiteral
    |   '(' ExpressionNoIn ')'
    |   Identifier
    |   ArrayLiteral
    |   Literal
    |   FunctionExpression"""
    p[0] = "PrimaryExpression"
    p[0] = list(p)


def p_Literal(p):
    """Literal : DECIMAL_INTEGER_LITERAL
    | HEX_INTEGER_LITERAL
    | STRING_LITERAL
    | BOOLEAN_LITERAL
    | FLOAT_LITERAL
    | NULL """
    p[0] = "Literal"
    p[0] = list(p)


def p_Identifier(p):
    """Identifier : IDENTIFIER_NAME"""
    p[0] = "Identifier"
    p[0] = list(p)


def p_ArrayLiteral(p):
    """ArrayLiteral : '[' ElementList ']'"""
    p[0] = "ArrayLiteral"
    p[0] = list(p)


def p_ElementList(p):
    """ElementList : ElementList_END_WITH_EX
    | ElementList_END_WITH_EX AssignmentExpressionNoIn """
    if len(p) == 3:
        p[1].append(p[2])
    p[0] = p[1]


def p_ElementList_END_WITH_EX(p):
    """ElementList_END_WITH_EX : AssignmentExpressionNoIn
    |   ','
    |   ElementList_END_WITH_EX AssignmentExpressionNoIn ','
    |   ElementList_END_WITH_EX ','"""
    if len(p) == 2:
        p[0] = ["ElementList", p[1]]
    elif len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    elif len(p) == 4:
        p[1].append(p[2])
        p[1].append(p[3])
        p[0] = p[1]


def p_ObjectLiteral(p):
    """ObjectLiteral : '{' PropertyNameAndValueList '}'
    | '{'  '}'"""
    p[0] = "ObjectLiteral"
    p[0] = list(p)


def p_PropertyNameAndValueList(p):
    """PropertyNameAndValueList : PropertyNameAndValue
    |  PropertyNameAndValueList ',' PropertyNameAndValue """
    if len(p) == 4:
        p[1].append(p[2])
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = ["PropertyNameAndValueList", p[1]]


def p_PropertyNameAndValue(p):
    """PropertyNameAndValue : PropertyName ':' AssignmentExpressionNoIn"""
    p[0] = "PropertyNameAndValue"
    p[0] = list(p)


def p_PropertyName(p):
    """PropertyName : Identifier
    |   STRING_LITERAL
    |   DECIMAL_INTEGER_LITERAL
    |   HEX_INTEGER_LITERAL
    |   FLOAT_LITERAL"""
    p[0] = "PropertyName"
    p[0] = list(p)


def p_MemberExpression(p):
    """MemberExpression : PrimaryExpression
    |   AllocationExpression
    |   MemberExpression MemberExpressionPart """
    p[0] = "MemberExpression"
    p[0] = list(p)


def p_AllocationExpression(p):
    """AllocationExpression : NEW MemberExpression Arguments"""
    p[0] = "AllocationExpression"
    p[0] = list(p)


def p_MemberExpressionPart(p):
    """MemberExpressionPart : '[' ExpressionNoIn ']'
    | '.' Identifier """
    p[0] = "MemberExpressionPart"
    p[0] = list(p)


def p_CallExpression(p):
    """CallExpression : MemberExpression Arguments
    | CallExpression Arguments
    | CallExpression MemberExpressionPart """
    p[0] = "CallExpression"
    p[0] = list(p)


def p_Arguments(p):
    """Arguments : '(' ArgumentList ')'
    | '('  ')'"""
    p[0] = "Arguments"
    p[0] = list(p)


def p_ArgumentList(p):
    """ArgumentList : AssignmentExpressionNoIn
    | ArgumentList ',' AssignmentExpressionNoIn """
    if len(p) == 4:
        p[1].append(p[2])
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = ["ArgumentList", p[1]]


def p_LeftHandSideExpression(p):
    """LeftHandSideExpression  ::= CallExpression
    |   MemberExpression """
    p[0] = "LeftHandSideExpression"
    p[0] = list(p)


def p_AssignmentExpressionNoIn(p):
    """AssignmentExpressionNoIn : LeftHandSideExpression EQUAL AssignmentExpressionNoIn
    | LeftHandSideExpression MUL_EQUAL AssignmentExpressionNoIn
    | LeftHandSideExpression DIV_EQUAL AssignmentExpressionNoIn
    | LeftHandSideExpression MOD_EQUAL AssignmentExpressionNoIn
    | LeftHandSideExpression PLUS_EQUAL AssignmentExpressionNoIn
    | LeftHandSideExpression MINUS_EQUAL AssignmentExpressionNoIn
    | LeftHandSideExpression SHIFT_LEFT_EQUAL AssignmentExpressionNoIn
    | LeftHandSideExpression SHIFT_RIGHT_ARITHMATIC_EQUAL AssignmentExpressionNoIn
    | LeftHandSideExpression SHIFT_RIGHT_LOGIC_EQUAL AssignmentExpressionNoIn
    | LeftHandSideExpression AND_EQUAL AssignmentExpressionNoIn
    | LeftHandSideExpression XOR_EQUAL AssignmentExpressionNoIn
    | LeftHandSideExpression OR_EQUAL AssignmentExpressionNoIn
    | AssignmentExpressionNoIn OR_OR AssignmentExpressionNoIn
    | AssignmentExpressionNoIn AND_AND AssignmentExpressionNoIn
    | AssignmentExpressionNoIn OR AssignmentExpressionNoIn
    | AssignmentExpressionNoIn XOR AssignmentExpressionNoIn
    | AssignmentExpressionNoIn AND AssignmentExpressionNoIn
    | AssignmentExpressionNoIn EQUAL_EQUAL AssignmentExpressionNoIn
    | AssignmentExpressionNoIn NOT_EQUAL AssignmentExpressionNoIn
    | AssignmentExpressionNoIn EQUAL_EQUAL_EQUAL AssignmentExpressionNoIn
    | AssignmentExpressionNoIn NOT_EQUAL_EQUAL AssignmentExpressionNoIn
    | AssignmentExpressionNoIn LESS_THAN AssignmentExpressionNoIn
    | AssignmentExpressionNoIn GREAT_THAN AssignmentExpressionNoIn
    | AssignmentExpressionNoIn LESS_EQUAL_THAN AssignmentExpressionNoIn
    | AssignmentExpressionNoIn GREAT_EQUAL_THAN AssignmentExpressionNoIn
    | AssignmentExpressionNoIn SHIFT_LEFT AssignmentExpressionNoIn
    | AssignmentExpressionNoIn SHIFT_RIGHT_ARITHMATIC AssignmentExpressionNoIn
    | AssignmentExpressionNoIn SHIFT_RIGHT_LOGIC AssignmentExpressionNoIn
    | AssignmentExpressionNoIn PLUS AssignmentExpressionNoIn
    | AssignmentExpressionNoIn MINUS AssignmentExpressionNoIn
    | AssignmentExpressionNoIn MUL AssignmentExpressionNoIn
    | AssignmentExpressionNoIn DIV AssignmentExpressionNoIn
    | AssignmentExpressionNoIn MOD AssignmentExpressionNoIn
    | PLUS_PLUS AssignmentExpressionNoIn %prec UNARY
    | MINUS_MINUS AssignmentExpressionNoIn %prec UNARY
    | TYPEOF AssignmentExpressionNoIn %prec UNARY
    | VOID AssignmentExpressionNoIn %prec UNARY
    | PLUS AssignmentExpressionNoIn %prec UNARY
    | MINUS AssignmentExpressionNoIn %prec UNARY
    | BIT_WISE_NOT AssignmentExpressionNoIn %prec UNARY
    | NOT AssignmentExpressionNoIn
    | AssignmentExpressionNoIn PLUS_PLUS %prec RIGHT_HAND
    | AssignmentExpressionNoIn MINUS_MINUS %prec RIGHT_HAND
    | LeftHandSideExpression %prec LEFT_HAND"""
    p[0] = "AssignmentExpressionNoIn"
    p[0] = list(p)


def p_ExpressionNoIn(p):
    """ExpressionNoIn : AssignmentExpressionNoIn
    | ExpressionNoIn ',' AssignmentExpressionNoIn"""
    p[0] = "ExpressionNoIn"
    p[0] = list(p)


def p_Statement(p):
    """Statement : Block
    |   VariableStatement
    |   EmptyStatement
    |   ExpressionNoInStatement
    |   IfStatement
    |   IterationStatement
    |   ReturnStatement
    |   PrintStatement"""
    p[0] = "Statement"
    p[0] = list(p)
    # printAST(list(p))


def p_StatementList(p):
    """StatementList : Statement
    |   StatementList Statement
    |   StatementList error"""
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = "StatementList"
        p[0] = list(p)
        # print("StatementList")


def p_VariableStatement(p):
    """VariableStatement : VAR Identifier ';'
    |   VAR Identifier EQUAL AssignmentExpressionNoIn ';' """
    p[0] = "VariableStatement"
    p[0] = list(p)
    # print("VariableStatement")


def p_VariableStatementError(p):
    """VariableStatement : VAR error ';'
    |   VAR error
    |   VAR Identifier EQUAL error ';'
    |   VAR Identifier EQUAL error"""
    p[0] = "VariableStatement"
    p[0] = list(p)


def p_EmptyStatement(p):
    """EmptyStatement : ';'"""
    p[0] = "EmptyStatement"
    p[0] = list(p)
    # print("EmptyStatement")


def p_ExpressionNoInStatement(p):
    """ExpressionNoInStatement : ExpressionNoIn ';' """
    p[0] = "ExpressionNoInStatement"
    p[0] = list(p)
    # print("ExpressionNoInStatement")


def p_ExpressionNoInStatementError(p):
    """ExpressionNoInStatement : error ';' """
    p[0] = "ExpressionNoInStatement"
    p[0] = list(p)


def p_IfStatement(p):
    """IfStatement : IF '(' ExpressionNoIn ')' Statement ELSE Statement
    |   IF '(' ExpressionNoIn ')' Statement """
    p[0] = "IfStatement"
    p[0] = list(p)


def p_IfStatementError(p):
    """IfStatement : IF '(' error ')' Statement ELSE Statement
    |   IF '(' error ')' Statement """
    p[0] = "IfStatement"
    p[0] = list(p)


def p_IterationStatement(p):
    """IterationStatement : DoStatement
    |   WhileStatement
    |   OriginForStatement
    |   ForEachStatement"""
    p[0] = "IterationStatement"
    p[0] = list(p)
    # print("IterationStatement")


def p_DoStatement(p):
    """DoStatement : DO Statement WHILE '(' ExpressionNoIn ')' ';' """
    p[0] = "DoStatement"
    p[0] = list(p)
    # print("DoStatement")


def p_DoStatementError(p):
    """DoStatement : DO Statement WHILE '(' error ')' ';' """
    p[0] = "DoStatement"
    p[0] = list(p)


def p_WhileStatement(p):
    """WhileStatement : WHILE '(' ExpressionNoIn ')' Statement """
    p[0] = "WhileStatement"
    p[0] = list(p)
    # print("WhileStatement")


def p_WhileStatementError(p):
    """WhileStatement : WHILE '(' error ')' Statement """
    p[0] = "WhileStatement"
    p[0] = list(p)


def p_OriginForStatement(p):
    """OriginForStatement : FOR '(' ExpressionNoIn  ';' ExpressionNoIn ';' ExpressionNoIn  ')' Statement """
    p[0] = "OriginForStatement"
    p[0] = list(p)


def p_OriginForStatementError(p):
    """OriginForStatement : FOR '(' ExpressionNoIn  ';' ExpressionNoIn ';' error ')' Statement
    |   FOR '(' ExpressionNoIn  ';' error ')' Statement
    |   FOR '(' error ')' Statement """
    p[0] = "OriginForStatement"
    p[0] = list(p)


def p_ForEachStatement(p):
    """ForEachStatement : FOR '(' VAR Identifier IN ExpressionNoIn ')' Statement"""
    p[0] = 'ForEachStatement'
    p[0] = list(p)


def p_ReturnStatement(p):
    """ReturnStatement : RETURN ExpressionNoIn ';'
    | RETURN ';' """
    p[0] = "ReturnStatement"
    p[0] = list(p)
    # print("ReturnStatement")


def p_ReturnStatementError(p):
    """ReturnStatement : RETURN error ';' """
    p[0] = "ReturnStatement"
    p[0] = list(p)


def p_PrintStatement(p):
    """PrintStatement : PRINT ExpressionNoIn ';' """
    p[0] = "PrintStatement"
    p[0] = list(p)


def p_FunctionExpression(p):
    """FunctionExpression : FUNCTION Identifier '(' FormalParameterList ')' FunctionBody
                    | FUNCTION Identifier '(' ')' FunctionBody
                    | FUNCTION '(' FormalParameterList ')' FunctionBody
                    | FUNCTION '(' ')' FunctionBody"""
    p[0] = 'FunctionExpression'
    p[0] = list(p)
    # print("FunctionExpression")


def p_FormalParameterList(p):
    """FormalParameterList : Identifier
                    | FormalParameterList ',' Identifier"""
    if len(p) == 4:
        p[1].append(p[2])
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = ['FormalParameterList', p[1]]


def p_FunctionBody(p):
    """FunctionBody : '{'  '}'
                    | '{' StatementList '}'"""
    p[0] = 'FunctionBody'
    p[0] = list(p)


def p_Program(p):
    """Program : StatementList"""
    p[0] = ["Program", p[1]]


def printAST(p, n=0):
    if p is not None:
        print('  ' * n, end='')
        if type(p) is list:
            print(p[0])
            for node in p[1:]:
                printAST(node, n + 1)
        else:
            print(p)


lexer = lex.lex()
lexer.lines = [0]


def build(start_label):
    yacc.yacc(debug=1, start=start_label, optimize=True, tabmodule="lift_tab")


def parse(source):
    ret = yacc.parse(source)
    reload(Inspector)
    Parser.correct = Inspector.inspect(ret) and Parser.correct
    # printAST(ret)
    return ret if Parser.correct else None


if __name__ == "__main__":
    build("Program")
    with open("error/basic.js") as file:
        ast = yacc.parse(file.read())
