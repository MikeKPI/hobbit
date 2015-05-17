from collections import OrderedDict
from copy import copy
from hobbit_lib.opg.unit import Unit


class RelationsTable:
    def __init__(self, table):
        self.table = table
        for i in table:
            i.buildPlus(Unit.LASTS)
            i.buildPlus(Unit.FIRSTS)
        tmp = OrderedDict([(i.token, '') for i in table])
        self.relations = OrderedDict([(i.token, copy(tmp)) for i in table])
    # TODO-me : create relation table using following algorithm
    #     1. Set '=' relations (needs to be passed).
    #     2. Setting '<' relations
    #        if Table[R][S] == '=' and \
    #               S.Firsts is not None:
    #           for i in S.Firsts:
    #               Table[R][i] = '<'
    #     3. Setting '>' relations
    #       if Table[R][S] == '=' and \
    #               R.Lasts is not None:
    #           for i in R.Lasts:
    #               if S.Firsts in None:
    #                   Table[i][S] = '>'
    #               else:
    #                   for j in S.Firsts:
    #                       Table[i][j] = '>'
