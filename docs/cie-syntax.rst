=========================
Syntax - Work in progress
=========================

Keywords
========
Keywords can be mixed case. Example WHILE, While, while are treated the same.

.. code-block::

    OR, AND, REPEAT, UNTIL, IF, THEN, ELSE, ENDIF, WHILE, DO, ENDWHILE, OUTPUT, INPUT, DECLARE, 
    PROCEDURE, ENDPROCEDURE, ARRAY, OF, CALL, FUNCTION, ENDFUNCTION, RETURNS, RETURN, FOR, TO,
    STEP, NEXT, CASE, ENDCASE, OTHERWISE, INTEGER, REAL, CHAR, STRING, BOOLEAN, DATE, TRUE, FALSE

Comments
========
Pseudocode comments are single line comments and begin with //

Example.

.. code-block::

    DECLARE Name : STRING // This is a string declaration


Data types
==========

Supported data types:

* INTEGER
    * whole numbers, example, 23 
* STRING
    * use double quotes (" ") to define strings, example, "Hello there"
* REAL                                
    * decimal numbers, example, 3.14
* BOOLEAN
    * boolean expressions evaluate to TRUE or FALSE
* DATE
    * example, 31/03/2000
* CHAR
    * use single quote (' ') to define a character, example, ‘c’

Variables
=========
Variables need to be declared before use, and can include letters, numbers or the underscore '_'. 
Variable names cannot start with a number and use the name of keywords.

To declare a variable use the DECLARE : *<data type>*

Example:

.. code-block::

    DECLARE MyVariable : INTEGER

NOTE THE USE OF THE ‘:’

Arrays
======
Array variables are one dimensional and each element is of the same type. They need to be declared before use.

.. code-block::

    DECLARE <variable name> : ARRAY [ n : m ] OF <datatype>

where n is the starting index, m is the ending index

Example.

.. code-block::

    DECLARE my_arr : ARRAY [ 1 : 10 ] OF INTEGER

Assignment 
==========
Use '<-', not '='

Example.

.. code-block::

    my_var <- 3

    my_array[ 2 ] <- 19


Input
=====
.. code-block::

    INPUT <variable>


Use Input to get data from the keyboard. Data is automatically converted to the data type delcared.

Example.
.. code-block::

    DECLARE price : REAL
    INPUT price


Output
======
.. code-block::

    OUTPUT expression1, expression2, ..., expressionn

Output writes data to the screen. Data is a list of expressions.

Example.
.. code-block::

    DECLARE name: STRING
    INPUT name
    OUTPUT "Your name is", name 


Operators
=========
    
Arithmetic operators:
---------------------

* \+
* \- 
* \*
* \/
* MOD()
* DIV()

Logical operators: 
------------------

* AND 
* OR 
* NOT  

Decision statements
====================

**IF** and **ELSE**
-------------------

.. code-block::

    IF a < b THEN:
        OUTPUT “a < b”
    ENDIF

Nested If statements
--------------------
.. code-block::

    IF a < b THEN:    
        OUTPUT “a < b”
    ELSE
        IF a > b THEN
            OUTPUT “a > b”
        ELSE
            OUTPUT “a = b”
        ENDIF
    ENDIF

Case statements
---------------
.. code-block::
    
    CASE OF <identifier>
        <value 1> : <statement>
        <value 2> : <statement>
        ...
    ENDCASE

    // An OTHERWISE clause can be the last case:

    CASE OF <identifier>
        <value 1> : <statement>
        <value 2> : <statement>
        ...
        OTHERWISE <statement>
    ENDCASE

Iteration (loops)
=================
There are three types of loop structures:

* WHILE .. DO … ENDWHILE
* REPEAT … UNTIL
* FOR … NEXT

While <condition> do *statements* endwhile
==========================================
While loops are known as pre-condition loop structures.
They will execute the body of the code while the condition is TRUE


.. code-block::

    DECLARE Num : INTEGER
    Num <- 1
    WHILE Num < 10 DO
        OUTPUT Num    
        Num <- Num + 1 
    ENDWHILE

Repeat *statements* UNTIL <condition>
=====================================
Repeat until loops are known as post-condition loop structures.
They will execute the body of the code until the condition becomes TRUE

.. code-block::

    DECLARE Num : INTEGER
    Num <- 1
    Repeat    
        OUTPUT Num    
        Num <- Num + 1
    UNTIL Num >= 10

FOR x <- x to y [step z] *statements* next
==========================================

.. code-block::

    FOR X <- 1 TO 10
      OUTPUT X
    NEXT X


