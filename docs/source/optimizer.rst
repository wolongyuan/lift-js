Optimizer
=========

.. toctree::
    :maxdepth: 2

Fold Constant
-------------

    为了使生成的中间代码执行起来更加高效，在编译时我们可以计算好一些常量的值。

::

    1 ＋ 2   ->  3

::

    'abc' + 'def'   ->  'abcdef'

::

    (1 + 2) ->  3

::

    5 > 2   ->  true

::

    return 1 + 2    ->  return 3

::

    f(1 + 2)    ->  f(3)
    

Eliminate Unreachable
---------------------

    Eliminate unreachable statements in if-statements and while-statements when the judge condition is constant. 

::

    var a;
    if(1)
        a = 5;
    else
        a = 8;

    will be optimized to

    var a;
    a = 5;

::

    var a;
    if(false)
        a = 5;
    else
        a = 8;

    will be optimized to

    var a;
    a = 8;

::

    var a;
    if(1)
        a = 5

    will be optimized to

    var a;
    a = 5;

::

    var a;
    if(0)
        a = 5

    will be optimized to

    var a;
    ;
    
::

    var a;
    while(0)
        a = 5;
    
    will be optimized to
    
    var a;
    ;
    

JIT
---

Workflow
++++++++

1. Discover all basic blocks.
2. Record the times of execution of each basic block.
3. If the times exceeds some predefined number, start optimizing.
4. The next time it is executed, use optimized code.
