Grammar
=======

.. toctree::
   :maxdepth: 2

Statement
---------

::
    
    Program : StatementList

::
    
    StatementList : Statement 
                  | StatementList Statement

::
    
    Statement : Block 
              | VariableStatement 
              | EmptyStatement 
              | ExpressionNoInStatement 
              | IfStatement 
              | IterationStatement 
              | ReturnStatement 
              | PrintStatement    

::
    
    EmptyStatement : ‘;’

::

    Block : ‘{‘ StatementList ‘}’ 
          | ‘{‘ ‘}’

::
    
    ReturnStatement : RETURN ExpressionNoIn ‘;’ 
                    | RETURN ExpressionNoIn 
                    | RETURN ‘;’ 
                    | RETURN

::
    
    PrintStatement : PRINT ExpressionNoIn ‘;’ 
                   | PRINT ExpressionNoIn

::
    
    VariableStatement : VAR Identifier ‘;’ 
                      | VAR Identifier 
                      | VAR Identifier EQUAL AssignmentExpressionNoIn 
                      | VAR Identifier EQUAL AssignmentExpressionNoIn ‘;’

::
    
    IfStatement : IF ‘(‘ ExpressionNoIn ‘)’ Statement ELSE Statement 
                | IF ‘(‘ ExpressionNoIn ‘)’ Statement

::
    
    IterationStatement : DoStatement 
                       | WhileStatement 
                       | OriginForStatement 
                       | ForEachStatement

::
    
    WhileStatement : WHILE ‘(‘ ExpressionNoIn ‘)’ Statement

::
    
    OriginForStatement : FOR ‘(‘ ExpressionNoIn ‘;’ ExpressionNoIn ‘;’ ExpressionNoIn ‘)’ Statement

::
    
    ForEachStatement : FOR ‘(‘ VAR Identifier IN ExpressionNoIn ‘)’ Statement

::

    DoStatement : DO Statement WHILE ‘(‘ ExpressionNoIn ‘)’ ‘;’ 
                | DO Statement WHILE ‘(‘ ExpressionNoIn ‘)’

::
    
    ExpressionNoInStatement : ExpressionNoIn ‘;’ 
                            | ExpressionNoIn

Function
--------

::
    
    FunctionExpression : FUNCTION Identifier ‘(‘ FormalParameterList ‘)’ FunctionBody 
                       | FUNCTION Identifier ‘(‘ ‘)’ FunctionBody 
                       | FUNCTION ‘(‘ FormalParameterList ‘)’ FunctionBody 
                       | FUNCTION ‘(‘ ‘)’ FunctionBody

::
    
    FunctionBody : ‘{‘ ‘}’ 
                 | ‘{‘ StatementList ‘}’                       

::
    
    FormalParameterList : Identifier 
                        | FormalParameterList ‘,’ Identifier

Expression
----------

::
    
    ExpressionNoIn : AssignmentExpressionNoIn 
                   | ExpressionNoIn ‘,’ AssignmentExpressionNoIn

::

    AssignmentExpressionNoIn : LeftHandSideExpression EQUAL AssignmentExpressionNoIn 
                             | LeftHandSideExpression MUL_EQUAL AssignmentExpressionNoIn 
                             | LeftHandSideExpression DIV_EQUAL AssignmentExpressionNoIn 
                             | LeftHandSideExpression MOD_EQUAL AssignmentExpressionNoIn 
                             | LeftHandSideExpression PLUS_EQUAL AssignmentExpressionNoIn 
                             | LeftHandSideExpression MINUS_EQUAL AssignmentExpressionNoIn 
                             | AssignmentExpressionNoIn SHIFT_LEFT_EQUAL AssignmentExpressionNoIn 
                             | AssignmentExpressionNoIn SHIFT_RIGHT_ARITHMATIC_EQUAL AssignmentExpressionNoIn 
                             | AssignmentExpressionNoIn SHIFT_RIGHT_LOGIC_EQUAL AssignmentExpressionNoIn 
                             | AssignmentExpressionNoIn AND_EQUAL AssignmentExpressionNoIn 
                             | AssignmentExpressionNoIn XOR_EQUAL AssignmentExpressionNoIn 
                             | AssignmentExpressionNoIn OR_EQUAL AssignmentExpressionNoIn 
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
                             | MemberExpression %prec RIGHT_HAND 
                             | AssignmentExpressionNoIn PLUS_PLUS %prec RIGHT_HAND 
                             | AssignmentExpressionNoIn MINUS_MINUS %prec RIGHT_HAND 
                             | LeftHandSideExpression %prec LEFT_HAND

::
    
    LeftHandSideExpression : Identifier 
                           | CallExpression 
                           | MemberExpression
                           
::
  
    MemberExpression : PrimaryExpression 
                     | AllocationExpression 
                     | MemberExpression MemberExpressionPart

::
  
    MemberExpressionPart : ‘[‘ ExpressionNoIn ‘]’ 
                         | ‘.’ Identifier

::

    AllocationExpression : NEW MemberExpression Arguments

::
  
    PrimaryExpression : THIS 
                      | ObjectLiteral 
                      | ‘(‘ ExpressionNoIn ‘)’ 
                      | Identifier 
                      | ArrayLiteral 
                      | Literal 
                      | FunctionExpression                                                            

::

    CallExpression : MemberExpression Arguments 
                   | CallExpression Arguments 
                   | CallExpression MemberExpressionPart                      

:: 

    Arguments : ‘(‘ ArgumentList ‘)’ 
              | ‘(‘ ‘)’

::

    ArgumentList : AssignmentExpressionNoIn 
                 | ArgumentList ‘,’ AssignmentExpressionNoIn

Literal
-------

::

    ArrayLiteral : ‘[‘ ElementList ‘]’

::

    ElementList : ElementList_END_WITH_EX 
                | ElementList_END_WITH_EX AssignmentExpressionNoIn

::

    ElementList_END_WITH_EX : AssignmentExpressionNoIn 
                            | ‘,’ 
                            | ElementList_END_WITH_EX AssignmentExpressionNoIn ‘,’ 
                            | ElementList_END_WITH_EX ‘,’

::
	
    Identifier : IDENTIFIER_NAME

::
	
    Literal : DECIMAL_INTEGER_LITERAL 
            | HEX_INTEGER_LITERAL 
            | STRING_LITERAL 
            | BOOLEAN_LITERAL 
            | FLOAT_LITERAL 
            | NULL

::
	
    ObjectLiteral : ‘{‘ PropertyNameAndValueList ‘}’ 
                  | ‘{‘ ‘}’

::
  
    PropertyNameAndValueList : PropertyNameAndValue 
                             | PropertyNameAndValueList ‘,’ PropertyNameAndValue

::
  
    PropertyNameAndValue : PropertyName ‘:’ AssignmentExpressionNoIn

::
	
    PropertyName : Identifier 
                 | STRING_LITERAL 
                 | DECIMAL_INTEGER_LITERAL 
                 | HEX_INTEGER_LITERAL 
                 | FLOAT_LITERAL
