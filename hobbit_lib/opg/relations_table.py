from hobbit_lib.opg.unit import Unit
from opg.grammar import grammar_elements


class RelationsTable:
    def __init__(self, grammar):
        self.grammar = grammar
        self.__find_elf()

    def __find_elf(self):
        """
        This methods find and all equals, first and lasts relations for given grammar.
        As result it build array with relations.
        """
        # Step 1 building relation array
        self._relations_array = [Unit(token=grammar_elements[token]) for token in grammar_elements]

        # Step 2 fill relation array element with equals, firsts and lasts relations
        for unit in self._relations_array:
            print(unit.token)
            if unit.token.language_id == -1:
                for rule in self.grammar[unit.token]:
                    unit.lasts.add(rule[-1])
                    unit.firsts.add(rule[0])
                    tmp_rule_len = len(rule)
                    if tmp_rule_len > 1:
                        for element_rule_idx in range(tmp_rule_len - 1):
                            self._relations_array[self._relations_array.index(rule[element_rule_idx])].equals.add(
                                self._relations_array[self._relations_array.index(rule[element_rule_idx+1])].token
                            )

        # Step 3 extends firsts and lasts to first_plus and last_plus
        for unit in self._relations_array:
            if unit.token.language_id == -1:
                continue
            unit.buildPlus(Unit.FIRSTS)
            unit.buildPlus(Unit.LASTS)

    def create_table(self):
        pass

    def find_lfs(self, lf_flag):
        pass
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

if __name__ == '__main__':
    from opg.grammar import grammar
    a = RelationsTable(grammar=grammar)
    for i in a._relations_array:
        print(i)
