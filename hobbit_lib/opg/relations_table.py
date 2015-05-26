from collections import OrderedDict
from copy import copy

from hobbit_lib.opg.unit import Unit


class RelationsTable:
    def __init__(self, grammar, grammar_elements):
        self.grammar = grammar
        self.grammar_elements = grammar_elements
        self.grammar_units = dict([
            (key, Unit(self.grammar_elements[key])) for key in self.grammar_elements
        ])
        self.__find_elf()
        self.__create_table()
        self.__fill_table()

    def __find_elf(self):
        """
        This methods find and all equals, first and lasts relations for given grammar.
        As result it build array with relations.
        """
        # Step 1 building relation array
        self._relations_dict = [Unit(token=self.grammar_elements[token]) for token in self.grammar_elements]

        # Step 2 fill relation array element with equals, firsts and lasts relations
        for unit in self._relations_dict:
            if unit.token.language_id == -1:
                for rule in self.grammar[unit.token]:
                    # print(rule[-1].name)
                    unit.lasts.add(self.grammar_units[rule[-1].name])
                    unit.firsts.add(self.grammar_units[rule[0].name])
                    tmp_rule_len = len(rule)
                    if tmp_rule_len > 1:
                        for element_rule_idx in range(tmp_rule_len - 1):
                            self._relations_dict[self._relations_dict.index(rule[element_rule_idx])].equals.add(
                                Unit(self._relations_dict[self._relations_dict.index(rule[element_rule_idx+1])].token)
                            )

        self._relations_dict = OrderedDict([(element.token, element)
                                            for element in self._relations_dict])

        # Step 3 extends firsts and lasts to first_plus and last_plus
        for i in range(44):
            for unit_key in self._relations_dict:
                if self._relations_dict[unit_key].token.language_id != -1:
                    continue
                self._build_first_plus(self._relations_dict[unit_key])
                self._build_last_plus(self._relations_dict[unit_key])

    def _build_first_plus(self, unit):
        tmp = copy(unit.firsts)
        for key in unit.firsts:
            tmp |= self._relations_dict[key.token].firsts
        unit.firsts = tmp

    def _build_last_plus(self, unit):
        tmp = copy(unit.lasts)
        for key in unit.lasts:
            tmp |= self._relations_dict[key.token].lasts
        unit.lasts = tmp

    def __create_table(self):
        """
        Creates 2 dimension dict based on grammar_elements.
        """
        self.relations_table = OrderedDict(
            [(self.grammar_elements[token], OrderedDict([(self.grammar_elements[token_inner], '')
                                                         for token_inner in self.grammar_elements]))
             for token in self.grammar_elements]
        )

    def __fill_table(self):
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

        # STEP 1 '=' relations
        for i in self._relations_dict:
            for j in self._relations_dict[i].equals:
                self.relations_table[self._relations_dict[i].token][j.token] += '='

        # STEP 2 '<' relations
        for R in self.relations_table:
            for S in self.relations_table[R]:
                if self.relations_table[R][S] == '=':
                    for i in self._relations_dict[S].firsts:
                        self.relations_table[R][i.token] += '<' if self.relations_table[R][i.token] != '<' else ''

        # STEP 3 '>' relations
        for R in self.relations_table:
            for S in self.relations_table[R]:
                if self.relations_table[R][S] == '=':
                    for i in self._relations_dict[R].lasts:
                        if len(self._relations_dict[S].firsts) == 0:
                            self.relations_table[i.token][S] += '>' if self.relations_table[i.token][S] != '>' else ''
                        else:
                            for j in self._relations_dict[S].firsts:
                                self.relations_table[i.token][j.token] += '>' if self.relations_table[i.token][j.token] != '>' else ''

        # STEP 4 adding blocking tokens
        tmp = create_non_terminal('#')
        for row in self.relations_table:
            self.relations_table[row][tmp] = '>'
        self.relations_table[tmp] = OrderedDict([(key, '<')
                                                 for key in self.relations_table])
        self.relations_table[tmp][tmp] = ''

    def __str__(self):
        temp = ' '
        answer = '{:3}{:40}|{}\n'.format(
            temp,
            temp,
            temp.join(['[{!s:3}]'.format(i) for i in range(1, len(self.relations_table)+1)])
        )
        for id, row in enumerate(self.relations_table):
            answer += '{:<3}{:40}|{}|\n'.format(
                id+1,
                row.name,
                ' '.join(['[{!s:3}]'.format(self.relations_table[row][cell])
                          for cell in self.relations_table[row]])
            )

        return answer


if __name__ == '__main__':
    from opg.grammar import grammar, grammar_elements, create_non_terminal

    a = RelationsTable(grammar=grammar, grammar_elements=grammar_elements)
    print(a)
    for i in a.relations_table:
        for j in a.relations_table[i]:
            if len(a.relations_table[i][j]) > 1:
                print(i, j, a.relations_table[i][j])
