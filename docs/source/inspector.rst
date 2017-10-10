Inspector
=========

.. toctree::
    :maxdepth: 2

Grammar
-------
    在语法层面，我们添加错误标记，使错误在一个Statement内被规约。通过这样的手段，所有的错误都被限定在Statement内，更为贴近用户的习惯。
    
::

    StatementList : StatementList error

::

    VariableStatement : VAR error ';'
                      | VAR error
                      | VAR Identifier EQUAL error ';'
                      | VAR Identifier EQUAL error
    ExpressionNoInStatement : error ';'
                      | error

::

    IfStatement : IF '(' error ')' Statement ELSE Statement
                | IF '(' error ')' Statement

::

    DoStatement : DO Statement WHILE '(' error ')' ';'

::

    WhileStatement : WHILE '(' ExpressionNoIn ')' Statement

::

    WhileStatement : WHILE '(' error ')' Statement

::

    OriginForStatement : FOR '(' ExpressionNoIn  ';' ExpressionNoIn ';' error ')' Statement
                       |   FOR '(' ExpressionNoIn  ';' error ')' Statement
                       |   FOR '(' error ')' Statement

Symbol Table
------------
    虽然我们建立了符号表，但是我们需要保存Javascript语言的动态性，为了不丢失任何Javascript的动态特性，我们将函数和变量视为同一种对象进行处理。同样我们也不能通过语义检查了审查代码的面向对象特性。因此我们只对局部变量进行审查，其检查方式依赖于函数直接的访问连接。该访问链接由scope栈实现，每当进入一个新函数时将其scope压入栈中，期本地变量都会被绑定在该scope上，当这个函数结束的时候，scope将会自动退栈。这样，我们就可以从栈低往栈顶搜索变量。

    ::


         ----------------      -------------
        |     program    | --> |  n  |  m  |
         ----------------      -------------------
        |  function g()  | --> |  i  |  j  |  m  |
         ----------------      -------------------
        |  function f()  | --> |  n  |
         ----------------      -------


