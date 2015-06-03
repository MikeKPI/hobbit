class Token:
    def __init__(self, name, call_action, value=None, reference=None):
        self.name = name
        self.value = value
        self._call = call_action
        self.reference = reference

    def __call__(self, *args, **kwargs):
        return self._call(self, *args, **kwargs)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash((self.name, self._call))

    def __str__(self):
        return str(self.name) if self.value is None else '<{}={!s}>'.format(self.name, self.value)

    def __repr__(self):
        return str(self.name)  # if self.value is None else '<{}={!s}>'.format(self.name, self.value)


if __name__ == '__main__':
    from hobbit_lib.rpn.call_actions import id_const_action, operator_action_decorator

    stack = [[]]
    source = [Token(name='7', call_action=id_const_action, value=7),
              Token(name='5', call_action=id_const_action, value=5),
              Token(name='+', call_action=operator_action_decorator(lambda a, b: a + b))]
    source_postion = 0

    while source_postion < len(source):
        source_postion = source[source_postion](stack, source, source_postion)
        print(stack)
