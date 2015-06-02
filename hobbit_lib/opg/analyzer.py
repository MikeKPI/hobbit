from copy import copy

from hobbit_lib.opg.relations_table import RelationsTable
from hobbit_lib.opg.grammar import create_non_terminal
from hobbit_lib.rpn.translator import get_RPNToken


class OPGAnalyzer:

    __LOG_ELEMENT_TEMPLATE = {
        'iteration': '',
        'stack': '',
        'relation': '',
        'input': '',
        'rpn': '',
    }

    def __init__(self, input_tokens_array, grammar, grammar_elements):
        self.log = []
        self.stack = []
        self.input = input_tokens_array
        self._relations_table = RelationsTable(grammar=grammar,
                                               grammar_elements=grammar_elements)
        print(self._relations_table)
        self._relations_table = self._relations_table.relations_table
        self.grammar = self._reverse_grammar(grammar=grammar)

    def analyze(self):
        self.stack.append(create_non_terminal('#'))
        self.input.append(create_non_terminal('#'))
        self.log.append(self._create_log_item(iteration=0, relation='<', rpn=[]))
        last_symbol = None
        for iteration in self._iteration_counter():
            rpn = copy(self.log[-1]['rpn'])
            flag = True
            if self.log[-1]['relation'] != '>' and flag:
                element = self.input[0]
                last_symbol = copy(element) if element.name != '#' else last_symbol
                relation = self._relations_table[self.stack[-1]][element]
                self.stack.append(element)
                self.input = self.input[1:]
            else:
                position = None
                for i in range(len(self.stack)-1, -1, -1):
                    if self._relations_table[self.stack[i-1]][self.stack[i]] == '<':
                        position = i
                        break

                if position is None:
                    raise Exception(last_symbol)

                try:
                    tmp_rule = tuple(self.stack[position:-1])
                    tmp_token = self.grammar[tmp_rule]
                    print(tmp_token, tmp_rule)
                    if tmp_token.name == '<value>' and self.stack[-3].name != '<data_type>':
                        rpn.append(get_RPNToken(tmp_rule[0]))
                    elif tmp_token.name == '<term>' and \
                                    len(tmp_rule) > 1:
                        rpn.append(get_RPNToken(tmp_rule[1]))
                    elif tmp_token.name == '<arithmetic_expression_body>':
                        t = len(tmp_rule)
                        if t == 2:
                            rpn.append(get_RPNToken(tmp_rule[0]))
                        elif t == 3:
                            rpn.append(get_RPNToken(tmp_rule[1]))
                    tmp = self.stack[-1]
                    self.stack = self.stack[:i-len(self.stack)]
                    self.stack.append(tmp_token)
                    self.input.insert(0, tmp)
                    self.log.append(self._create_log_item(iteration=iteration,
                                                          relation=self._relations_table[self.stack[-2]][
                                                              self.stack[-1]],
                                                          rpn=copy(rpn)))
                    yield self.log[-1]
                    continue
                except KeyError:
                    if tmp_rule[0] == create_non_terminal('<main>') and\
                            len(tmp_rule) == 1:
                        break
                    raise Exception(last_symbol)

            self.log.append(self._create_log_item(iteration=iteration,
                                                  relation=relation,
                                                  rpn=rpn))
            yield (self.log[-1])

    def _create_log_item(self, iteration, relation, rpn=None):
        tmp = copy(self.__LOG_ELEMENT_TEMPLATE)
        tmp['iteration'] = iteration
        tmp['stack'] = copy(self.stack)
        tmp['relation'] = relation
        tmp['input'] = copy(self.input)
        tmp['rpn'] = [] if rpn is None else rpn
        return tmp

    def _iteration_counter(self):
        tmp = 1
        while True:
            yield tmp
            tmp += 1

    @staticmethod
    def _reverse_grammar(grammar):
        tmp = dict()
        for token in grammar:
            for rule in grammar[token]:
                tmp[tuple(rule)] = token
        return tmp

if __name__ == '__main__':
    from hobbit_lib.tokenizer.tokenizer import Tokenizer
    from hobbit_lib.opg.grammar import grammar_elements, grammar

    with open('/Users/mike/input1.hobbit') as ifile:
        tokenizer = Tokenizer(source_to_analyze=ifile)
        input_array = tokenizer.analyze()['tokens']
        analyzer = OPGAnalyzer(input_tokens_array=input_array,
                               grammar=grammar,
                               grammar_elements=grammar_elements)
        try:
            t = [i for i in analyzer.analyze()]
            for i in t:
                print(i)

            from hobbit_lib.rpn.executor import execute

            print(execute(t[-1]['rpn']))

            print('OK')
        except Exception as e:
            print(e)
            # print('At line {!s} you have an error in symbol {}'.format(e.args[0].line_number + 1, e.args[0].name))
