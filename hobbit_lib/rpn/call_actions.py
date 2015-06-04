from copy import copy

from hobbit_lib.rpn.token import Token as RPNToken

values = dict()


def id_const_action(self, stack, source, source_position):
    stack[0].append(source[source_position])
    try:
        if values[stack[0][-1]] is not None:
            stack[0][-1].value = values[stack[0][-1]]
        else:
            raise KeyError
    except KeyError:
        if not isinstance(stack[0][-1].name, int):
            values[stack[0][-1]] = stack[0][-1].value
    return source_position + 1


def operator_action_decorator(function):
    def operator_action(self, stack, source, source_position):
        a = stack[0][-2].value if stack[0][-2] not in values else values[stack[0][-2]]
        b = stack[0][-1].value if stack[0][-1] not in values else values[stack[0][-1]]
        stack[0] = stack[0][:-1]
        t_val = function(a, b)
        if t_val.__class__.__name__ != 'int':
            stack[0][-1] = copy(stack[0][-1])

        stack[0][-1] = RPNToken(name=str(t_val),
                                call_action=id_const_action,
                                value=t_val)
        return source_position + 1

    return operator_action


def unary_minus_action(self, stack, source, source_position):
    stack[0][-1] = RPNToken(name=str(-stack[0][-1].value),
                            call_action=id_const_action,
                            value=-stack[0][-1].value)
    values[stack[0][-1]] = stack[0][-1].value
    return source_position + 1


def round_brace_action(self, stack, source, source_position):
    stack[0] = stack[0][:-1]
    return source_position + 1


def set_action(self, stack, source, source_position):
    values[stack[0][-2]] = stack[0][-1].value
    stack[0] = stack[0][:-2]
    return source_position + 1


def output_action(self, stack, source, source_position):
    print("hobbit output {}: ".format(stack[0][-1].name), stack[0][-1].value)
    stack[0] = stack[0][:-1]
    return source_position + 1


def input_action(self, stack, source, source_position):
    values[stack[0][-1]] = eval(input("hobbit input {}: ".format(stack[0][-1].name)))
    stack[0] = stack[0][:-1]
    return source_position + 1


def UPL(self, stack, source, source_position):
    t = source_position + 1 if stack[0][-1].value else source.index(self.reference)
    stack[0] = stack[0][:-2]
    return t


def BP(self, stack, source, source_position):
    t = source.index(self.reference)
    stack[0] = stack[0][:-2]
    return t

def next_item(self, stack, source, source_position):
    if source_position > len(source):
        return source_position
    return source_position + 1