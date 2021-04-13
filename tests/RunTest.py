import sys, os

sys.path += ['pseudonaja']
print(os.getcwd())

import pseudonaja.c.PInterpreter as pscint
import json

class RunTest:

    class Keyboard:
        def __init__(self, inputs):
            self.lines = inputs
            self.count = -1

        def readline(self):
            self.count += 1
            return self.lines[self.count]

    class Screen:
        def __init__(self):
            self.lines = []

        def write(self, line):
            self.lines.append(line)

        def flush(self):
            '''

            '''
            pass
        def __str__(self):
            return "".join(self.lines)

        def compare(self, name, outputs, screen):

            outputs = "".join(outputs)
            '''
            def dump(a, e):
                for i, c in enumerate(a):
                    print(f"{i} a={c} e={outputs[i] if i < len(outputs) else None}")

            dump(''.join(self.lines), outputs)
            '''
            assert ''.join(self.lines) == outputs, f"Test failed ({name})\n\nTest output\n{screen}\n\nExpected output\n{outputs}"
            print(f"Test ({name}) successful")


    def __init__(self, testfile):

        # read file
        with open(testfile+".json", 'r') as t:
            data = t.read()

        # parse file
        test = json.loads(data)

        import sys
        sys.stdin = RunTest.Keyboard(test['inputs'])

        stdout_save = sys.stdout
        s = RunTest.Screen()
        sys.stdout = s

        pscint.PInterpreter().run('\n'.join(test['code']))

        sys.stdout = stdout_save

        s.compare(test['name'], test['outputs'], s)

if __name__ == "__main__":
    RunTest("pseudonaja/tests/Test4")