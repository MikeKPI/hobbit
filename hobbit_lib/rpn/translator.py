from hobbit_lib.rpn.token import Token as RPNToken
from hobbit_lib.opg.grammar import grammar_elements
from hobbit_lib.rpn.call_actions import id_const_action, operator_action_decorator, unary_minus_action

PRIORITIES = dict([
    (grammar_elements["ID"], -100),
    (grammar_elements["CONST"], -100),
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
             grammar_elements['@']]


def get_RPNToken(token):
    if token.name == 'ID':
        return RPNToken(name=token.name_value,
                        value=token.value,
                        call_action=id_const_action)
    elif token.name == 'CONST':
        return RPNToken(name=token.name_value,
                        value=token.value,
                        call_action=id_const_action)
    elif token.name in SPLITTERS:
        pass
    elif token.name != '@':
        return RPNToken(name=token,
                        call_action=operator_action_decorator(eval('lambda a, b: a {} b'
                                                                   .format(token))))
    else:
        return RPNToken(name=token,
                        call_action=unary_minus_action)


def translate(source):
    rpc = []
    stack = []

    for token in source:
        round_brace_flag = True
        print(stack)
        if token.name == 'ID' or \
                        token.name == 'CONST':

            rpc.append(get_RPNToken(token))

        else:
            while len(stack) > 0 and \
                            PRIORITIES[stack[-1]] >= PRIORITIES[token]:
                if token.name == '(':
                    break

                tmp = get_RPNToken(stack[-1])
                if tmp is not None:
                    rpc.append(tmp)
                if token.name == ')':
                    round_brace_flag = False
                    stack = stack[:-1 if stack[-2] in OPERATORS else -2] if len(stack) > 1 else []
                else:
                    stack = stack[:-1] if len(stack) > 1 else []

            if round_brace_flag:
                stack.append(token)

    for i in stack[::-1]:
        tmp = get_RPNToken(i)
        if tmp is not None:
            rpc.append(tmp)

    return rpc


if __name__ == '__main__':
    from hobbit_lib.tokenizer.tokenizer import Tokenizer
    from hobbit_lib.rpn.executor import execute

    with open('/Users/mike/input.hobbit') as ifile:
        tokenizer = Tokenizer(source_to_analyze=ifile)
        a = tokenizer.analyze()['tokens'][15:27]
        print(a)
        source = translate(a)
        print(source)
        execute(source)
