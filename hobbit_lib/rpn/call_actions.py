def id_const_action(self, stack, source, source_position):
    stack[0].append(self.value)
    return source_position + 1


def operator_action_decorator(function):
    def operator_action(self, stack, source, source_position):
        a = stack[0][-2]
        b = stack[0][-1]
        stack[0] = stack[0][:-2]
        stack[0].append(function(a, b))
        return source_position + 1

    return operator_action


def unary_minus_action(self, stack, source, source_position):
    stack[0][-1] = -stack[0][-1]
    return source_position + 1


def round_brace_action(self, stack, source, source_position):
    stack[0] = stack[0][:-1]
    return source_position + 1

# def if_cycle_start_action(self, stack, source, source_position):
