from copy import copy
from hobbit_lib.rpn.token import Token as RPNToken
from hobbit_lib.opg.grammar import grammar_elements, create_terminal
from hobbit_lib.rpn.call_actions import id_const_action, operator_action_decorator, unary_minus_action, \
    set_action, output_action, input_action, UPL, next_item, BP
from hobbit_lib.tokenizer.common.alphabet import Alphabet
from opg.token import Token

PRIORITIES = dict([
    ("{", 1),
    ("(", 1),
    ("for", 1),
    ("if", 1),

    ("}", 2),
    (")", 2),
    (r"\n", 2),
    ("to", 2),
    ("do", 2),

    ("in", 3),
    ("out", 3),
    ("=", 3),

    (">", 7),
    ("<", 7),
    (">=", 7),
    ("<=", 7),
    ("!=", 7),
    ("==", 7),

    ("@", 10),

    ("+", 9),
    ("-", 9),

    ("*", 10),
    ("%", 10),
    ("/", 10)
])

SPLITTERS = ['{', '}', '(', ')', '\n']
OPERATORS = [grammar_elements['+'],
             grammar_elements['-'],
             grammar_elements['/'],
             grammar_elements['*'],
             grammar_elements['%'],
             grammar_elements['@'],
             grammar_elements['<'],
             grammar_elements['>'],
             grammar_elements['=='],
             grammar_elements['!='],
             grammar_elements['>='],
             grammar_elements['<='], ]


class Translator:
    def __init__(self):
        self.constants = dict()
        self.variables = dict()
        self.curent_pointer = 0

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
            return RPNToken(name=token.name,
                            call_action=set_action)
        elif token in OPERATORS and token.name != '@':
            return RPNToken(name=token.name,
                            call_action=operator_action_decorator(eval('lambda a, b: a {} b'
                                                                       .format(token))))
        elif token.name == '@':
            return RPNToken(name=token.name,
                            call_action=unary_minus_action)
        elif token.name == 'out':
            return RPNToken(name=token.name,
                            call_action=output_action)
        elif token.name == 'in':
            return RPNToken(name=token.name,
                            call_action=input_action)
        elif token.name == '#':
            t_name = copy(token.name) + str(self.curent_pointer)
            t = RPNToken(name=t_name,
                         call_action=next_item)
            self.curent_pointer += 1
            return t
        elif token.name == 'UPL':
            t = RPNToken(name=token.name,
                         call_action=UPL)
            return t
        elif token.name == 'BP':
            t = RPNToken(name=token.name,
                         call_action=BP)
            return t
        elif token.name == 'for':
            refs = [self.get_RPNToken(create_terminal('#', '-1')) for _ in range(2)]
            for i in range(2):
                refs[i].name += ':'

            t = RPNToken(name=token.name,
                         call_action=next_item,
                         reference=refs)
            return t

    def translate(self, source):
        rpc = []
        stack = []
        data_type_flag = False
        cycle_flag = False
        cycle_iterator = []

        for token in source:
            round_brace_flag = True
            skip = True if token.name == r'\n' or token.name == '{' else False

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
                t = self.get_RPNToken(token)
                rpc.append(t)
                if cycle_flag:
                    cycle_iterator.append(t)
                    cycle_flag = False
            elif token.name == 'do':
                rpc.append(self.get_RPNToken(create_terminal('<=', -1)))
                t = copy(stack[-1].reference[-1])
                t.name = t.name[:-1]
                rpc.append(t)
                rpc.append(self.get_RPNToken(create_terminal('UPL', -1)))
                rpc[-1].reference = stack[-1].reference[-1]
            else:
                while len(stack) > 0 and \
                                PRIORITIES[stack[-1].name] >= PRIORITIES[token.name]:
                    if token.name == 'for' and stack[-1].name == 'if':
                        break
                    if token.name != '}' and stack[-1].name == 'for':
                        break
                    if token.name == '(':
                        break
                    elif token.name == '{' and stack[-1].name == 'for':
                        break
                    elif token.name == 'to':
                        rpc.append(self.get_RPNToken(stack[-1]))
                        rpc.append(stack[-2].reference[0])
                        rpc.append(cycle_iterator[-1])
                        stack = stack[:-1]
                        continue
                    elif token.name == '{' and stack[-1].name == 'if':
                        rpc.append(self.get_RPNToken(create_terminal('#', -1)))
                        rpc.append(self.get_RPNToken(create_terminal('UPL', -1)))
                        tmp = copy(rpc[-2])
                        tmp.name += ':'
                        tmp._call = next_item
                        rpc[-1].reference = tmp
                        stack[-1] = RPNToken(name=stack[-1].name,
                                             call_action=next_item,
                                             reference=tmp)
                        break
                    elif token.name == 'do':
                        rpc.append(self.get_RPNToken(create_terminal('<=', -1)))
                        t = copy(stack[-1].reference[-1])
                        t.name = t.name[:-1]
                        rpc.append(t)
                        rpc.append(self.get_RPNToken(create_terminal('UPL', -1)))
                        rpc[-1].reference = stack[-1].reference[-1]

                    tmp = self.get_RPNToken(stack[-1])
                    if tmp is not None:
                        rpc.append(tmp)
                    if token.name == ')':
                        round_brace_flag = False
                        stack = stack[:-1 if stack[-2] in OPERATORS else -2] if len(stack) > 1 else []
                        break
                    else:
                        stack = stack[:-1] if len(stack) > 1 else []

                if skip:
                    continue

                if round_brace_flag:
                    if token.name == ')':
                        rpc.append(self.get_RPNToken(stack[-2]))
                        stack = stack[:-2]
                    elif token.name == '}' and len(stack) > 0:
                        if stack[-1].name == 'if':
                            rpc.append(stack[-1].reference)
                            stack = stack[:-1] if len(stack) > 1 else []
                        elif stack[-1].name == 'for':
                            rpc.append(cycle_iterator[-1])
                            rpc.append(cycle_iterator[-1])
                            tmp = Token(name=1, type='int', line_number=-1, language_id=-1)
                            tmp.value = 1
                            tmp.name = 'CONST'
                            rpc.append(self.get_RPNToken(tmp))
                            rpc.append(self.get_RPNToken(create_terminal('+', -1)))
                            rpc.append(self.get_RPNToken(create_terminal('=', -1)))
                            t = copy(stack[-1].reference[0])
                            t.name = t.name[:-1]
                            rpc.append(t)
                            rpc.append(self.get_RPNToken(create_terminal('BP', -1)))
                            rpc[-1].reference = stack[-1].reference[0]
                            rpc.append(stack[-1].reference[-1])
                            stack = stack[:-1]
                            cycle_iterator = cycle_iterator[:-1]
                    else:
                        if token.name == 'for':
                            stack.append(self.get_RPNToken(token))
                            cycle_flag = True
                        elif token.name == 'to':
                            continue
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
        print(source)
        print('EXECUTE...')
        execute(source)
