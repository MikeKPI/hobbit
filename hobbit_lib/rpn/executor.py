def execute(source):
    stack = [[]]
    source_postion = 0
    while source_postion < len(source):
        # print(source[source_postion])
        source_postion = source[source_postion](stack, source, source_postion)

    if len(stack[0]) == 1:
        return stack[0][0]
    else:
        return 'Wrong source {!s}'.format(source)
