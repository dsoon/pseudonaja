=====
Usage
=====

To use pseudonaja in a project::

    import pseudonaja.c.PInterpreter as interpreter
    interpreter.PInterpreter().repl()

    // or

    import pseudonaja.c.PInterpreter as interpreter

    PROG = '''\
        output "Hello World!"
    '''
    interpreter.PInterpreter().run(PROG)
