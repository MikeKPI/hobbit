def id_const_action(self, stack, source, source_position):
    stack[0].append(self)
    return source_position + 1


def operator_action_decorator(function):
    def operator_action(self, stack, source, source_position):
        a = stack[0][-2].value
        b = stack[0][-1].value
        stack[0] = stack[0][:-1]
        stack[0][-1].value = function(a, b)
        return source_position + 1

    return operator_action


def unary_minus_action(self, stack, source, source_position):
    stack[0][-1].value = -stack[0][-1].value
    return source_position + 1


def round_brace_action(self, stack, source, source_position):
    stack[0] = stack[0][:-1]
    return source_position + 1


def set_action(self, stack, source, source_position):
    stack[0][-2].value = stack[0][-1].value
    stack[0] = stack[0][:-2]
    return source_position + 1


def output_action(self, stack, source, source_position):
    print("hobbit output: ", stack[0][-1].value)
    stack[0] = stack[0][:-1]
    return source_position + 1


def input_action(self, stack, source, source_position):
    stack[0][-1].value = eval(input("hobbit input: "))
    stack[0] = stack[0][:-1]
    return source_position + 1


def UPL(self, stack, source, source_position):
    t = source_position + 1 if stack[0][-2].value else source.index(self.reference)
    stack[0] = stack[0][:-2]
    return t


def next_item(self, stack, source, source_position):
    return source_position + 1
