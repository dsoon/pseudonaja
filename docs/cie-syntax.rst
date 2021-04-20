===================================
Supported syntax - Work in progress
===================================

Cambridge IGCSE (9–1) Computer Science 0984 from 2019



Keywords
========
Keywords can be mixed case. Example WHILE, While, while are treated the same.

.. code-block::

    OR, AND, REPEAT, UNTIL, IF, THEN, ELSE, ENDIF, WHILE, DO, ENDWHILE, OUTPUT, INPUT, DECLARE, 
    PROCEDURE, ENDPROCEDURE, ARRAY, OF, CALL, FUNCTION, ENDFUNCTION, RETURNS, RETURN, FOR, TO,
    STEP, NEXT, CASE, ENDCASE, OTHERWISE, INTEGER, REAL, CHAR, STRING, BOOLEAN, DATE, TRUE, FALSE,
    CONSTANT

Case sensitivity
================
Keywords are reserved names and can be mixed case. That is, Repeat, repeat and REPEAT are all the 
same keyword.

Indentation
===========
While indentation is not required it is good practice to include indentation to show which statements
are part of the same block. Four spaces is recommended.

Comments
========
Comments are single line comments and begin with //. Everything after the '//' to the end of the line
will be ignored by the interpreter.

Example.

.. code-block::

    DECLARE Name : STRING // This is a string declaration


Data types
==========

The following datetypes are supported.

* INTEGER
    * whole numbers, example, 23 
* STRING
    * use double quotes (" ") to define strings, example, "Hello there"
* REAL                                
    * decimal numbers, example, 3.14
* BOOLEAN
    * boolean expressions evaluate to TRUE or FALSE
* DATE
    * example, "31/03/2000"
* CHAR
    * use single quotes (' ') to define a single character, example, 'c'

Variables
=========
Variables have to be declared before use, and names can include letters, numbers or the 
underscore '_'.  Variable names cannot start with a number and use the name of keywords.

To declare a variable use the DECLARE : *<data type>*

Example:

.. code-block::

    DECLARE MyVariable : INTEGER

NOTE THE USE OF THE ‘:’

Constants
=========
For literal values that don't change it is recommended that you define a constant for this value.
Constants can only be defined once and cannot be redefined when the program is executing. Constants
can be any of the data types supported.

Example:

.. code-block::

    CONSTANT PI = 3.14

Note the use of the '=' operator after the names. 


Arrays
======
Array variables are one dimensional and each element is of the same type. They need to be declared 
before use.

.. code-block::

    DECLARE <variable name> : ARRAY [ n : m ] OF <datatype>

where n is the starting index and can be any value, m is the ending index and must be greater than n

Example. To define an array of 10 integers use the folowing declaration.

.. code-block::

    DECLARE my_arr : ARRAY [ 1 : 10 ] OF INTEGER


Assignment 
==========
To set a variable use the '<-', not '=' operator.

Example.

.. code-block::

    // assign a value of three to the integer variable 'my_var'
    my_var <- 3

    // assign a value of 18 to the second index of my_array
    my_array[ 2 ] <- 19


Input
=====

Use the Input statement to get data from the keyboard. Data is automatically converted to the data 
type of the variable.

.. code-block::

    // Usage
    INPUT <variable>

Example.

.. code-block::

    DECLARE price : REAL
    INPUT price

The Input statement will wait until the use types a value followed by 'enter' This value is then
automatically assigned to the variable.


Output
======
Output writes data to the screen. Data is a list of expressions.

.. code-block::

    // Usage
    OUTPUT expression1, expression2, ..., expressionn


Example.
.. code-block::

    DECLARE name: STRING
    INPUT name
    OUTPUT "Your name is", name 


Operators
=========

These are the supported arithmetic and local operators.
    
Arithmetic operators:
---------------------

* \+
    * Addition operator
* \- 
    * Subtraction operator
* \*
    * Multiply operator
* \/
    * Divide operator - result will always be a REAL
* MOD(a, b)
    * Returns the value of 'a MOD b', example, MOD(16, 9) returns 7
* DIV(a, b)
    * Returns the integer value of a DIV b, example, DIV(5, 2) returns 2
* LEN(array)
    * Use this to return the length of a previously define array
* RANDOM(a, b)
    * USe this to return a random number from a to b, example, RANDOM(1, 100) returns a number 
    * between 1 and 100 inclusive.

Logical operators: 
------------------

* AND 
    * Logical AND, returns a BOOLEAN value, example 5 > 4 AND 6 = 6 will return True 
* OR
    * Logical OR, returns a BOOLEAN value, example 5 > 4 OR 7 <> 7 will return True 

Decision statements
====================

**IF** and **ELSE**
-------------------

Use if-then-endif to make a coding decision. If the <condition> evaluates to True, statements 1 ..name
are executed.

.. code-block::

    // Usage
    IF <condition> THEN
        <statement 1>
        <statement 2>
        ...
        <statement n>
    ENDIF


Example
.. code-block::

    IF a < b THEN
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

Procedures
==========
Procedures are used to group statements together, which can be called under a single name. 
Procedures can also be defined with parameters which can be passed when calling the procedure. Just
like variables, procedures need to be defined before being called.

Procedure declaration without parameters
----------------------------------------

.. code-block::
    PROCEDURE <name>
        <statement 1>
        <statement 2>
        ...
        <statement n>
    ENDPROCEDURE

Calling a procedure
-------------------

.. code-block::
    CALL <name>


Procedure declaration with parameters
-------------------------------------

.. code-block::
    PROCEDURE <name> ( num1 : INTEGER, num2: INTEGER)
        <statement 1>
        <statement 2>
        ...
        <statement n>
    ENDPROCEDURE

Calling a procedure
-------------------

.. code-block::
    CALL <name>


