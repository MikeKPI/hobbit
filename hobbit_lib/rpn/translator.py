from hobbit_lib.rpn.token import Token as RPNToken
from hobbit_lib.opg.grammar import grammar_elements
from hobbit_lib.rpn.call_actions import id_const_action, operator_action_decorator, unary_minus_action, \
    set_action, output_action, input_action
from hobbit_lib.tokenizer.common.alphabet import Alphabet

PRIORITIES = dict([
    (grammar_elements["{"], 1),
    (grammar_elements["("], 1),
    (grammar_elements["do"], 1),
    (grammar_elements["if"], 1),

    (grammar_elements["}"], 2),
    (grammar_elements[")"], 2),
    (grammar_elements[r"\n"], 2),
    (grammar_elements['else'], 2),

    (grammar_elements["in"], 3),
    (grammar_elements["out"], 3),
    (grammar_elements["="], 3),

    (grammar_elements[">"], 7),
    (grammar_elements["<"], 7),
    (grammar_elements[">="], 7),
    (grammar_elements["<="], 7),
    (grammar_elements["!="], 7),
    (grammar_elements["=="], 7),

    (grammar_elements["@"], 8),

    (grammar_elements["+"], 9),
    (grammar_elements["-"], 9),

    (grammar_elements["*"], 10),
    (grammar_elements["/"], 10)
])

SPLITTERS = ['{', '}', '(', ')', '\n']
OPERATORS = [grammar_elements['+'],
             grammar_elements['-'],
             grammar_elements['/'],
             grammar_elements['*'],
             grammar_elements['%'],
             grammar_elements['@'], ]


class Translator:
    def __init__(self):
        self.constants = dict()
        self.variables = dict()

    def get_RPNToken(self, token):
        if token.name == 'ID':
            if token.name_value in self.variables:
                return self.variables[token.name_value]
            else:
                t = RPNToken(name=token.name_value,
                             value=token.value,
                             call_action=id_const_action)
                self.variables[token.name_value] = t
                return t
        elif token.name == 'CONST':
            return RPNToken(name=token.name_value,
                            value=token.value,
                            call_action=id_const_action)
        elif token.name in SPLITTERS:
            pass
        elif token.name == '=':
            return RPNToken(name=token,
                            call_action=set_action)
        elif token in OPERATORS and token.name != '@':
            return RPNToken(name=token,
                            call_action=operator_action_decorator(eval('lambda a, b: a {} b'
                                                                       .format(token))))
        elif token.name == '@':
            return RPNToken(name=token,
                            call_action=unary_minus_action)
        elif token.name == 'out':
            return RPNToken(name=token.name,
                            call_action=output_action)
        elif token.name == 'in':
            return RPNToken(name=token.name,
                            call_action=input_action)

    def translate(self, source):
        rpc = []
        stack = []
        data_type_flag = False

        for token in source:
            print('{!s:40}{!s:40}{!s:40}'.format(token, rpc, stack))
            round_brace_flag = True

            if token.name == 'main':
                continue
            elif Alphabet.isDataType(token):
                data_type_flag = True
                continue
            elif data_type_flag:
                data_type_flag = False
                continue

            if token.name == 'ID' or \
                            token.name == 'CONST':

                rpc.append(self.get_RPNToken(token))

            else:
                while len(stack) > 0 and \
                                PRIORITIES[stack[-1]] >= PRIORITIES[token]:
                    if token.name == '(':
                        break

                    tmp = self.get_RPNToken(stack[-1])
                    if tmp is not None:
                        rpc.append(tmp)
                    if token.name == ')':
                        round_brace_flag = False
                        stack = stack[:-1 if stack[-2] in OPERATORS else -2] if len(stack) > 1 else []
                        break
                    else:
                        stack = stack[:-1] if len(stack) > 1 else []

                if round_brace_flag:
                    if token.name == ')':
                        rpc.append(self.get_RPNToken(stack[-2]))
                        stack = stack[:-2]
                    else:
                        stack.append(token)

        for i in stack[::-1]:
            tmp = self.get_RPNToken(i)
            if tmp is not None:
                rpc.append(tmp)

        return rpc


if __name__ == '__main__':
    from hobbit_lib.tokenizer.tokenizer import Tokenizer
    from hobbit_lib.rpn.executor import execute

    with open('/Users/mike/input1.hobbit') as ifile:
        tokenizer = Tokenizer(source_to_analyze=ifile)
        t = tokenizer.analyze()
        a = t['tokens']
        b = t['constants']
        c = t['variables']
        print(t)
        source = Translator().translate(a)

        print('\n\n\n\n')

        print(source)
        execute(source)
