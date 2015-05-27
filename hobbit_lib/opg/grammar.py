from collections import OrderedDict

from opg.token import Token

create_non_terminal = lambda name: Token(name=name, type='', line_number=0, language_id=-1)
create_terminal = lambda name, language_id: Token(name=name, type='', line_number=0, language_id=language_id)

grammar_elements = OrderedDict([
    ('<main>', create_non_terminal('<main>')),
    ('<block>', create_non_terminal('<block>')),
    ('<data_type>', create_non_terminal('<data_type>')),
    ('<param_list>', create_non_terminal('<param_list>')),
    ('<value>', create_non_terminal('<value>')),
    ('<variable>', create_non_terminal('<variable>')),
    ('<data_type>', create_non_terminal('<data_type>')),
    ('<block>', create_non_terminal('<block>')),
    ('<block_body>', create_non_terminal('<block_body>')),
    ('<block_body1>', create_non_terminal('<block_body1>')),
    ('<source_code_string>', create_non_terminal('<source_code_string>')),
    ('<sc_element>', create_non_terminal('<sc_element>')),
    ('<inp>', create_non_terminal('<inp>')),
    ('<out>', create_non_terminal('<out>')),
    ('<for_cycle>', create_non_terminal('<for_cycle>')),
    ('<if_expression>', create_non_terminal('<if_expression>')),
    ('<arithmetic_expression>', create_non_terminal('<arithmetic_expression>')),
    ('<bool_expression>', create_non_terminal('<bool_expression>')),
    ('<arithmetic_expression_body>', create_non_terminal('<arithmetic_expression_body>')),
    ('<arithmetic_expression_body1>', create_non_terminal('<arithmetic_expression_body1>')),
    ('<arithmetic_expression_body2>', create_non_terminal('<arithmetic_expression_body2>')),
    ('<term>', create_non_terminal('<term>')),
    ('<term1>', create_non_terminal('<term1>')),
    ('<multiplier>', create_non_terminal('<multiplier>')),
    ('<multiplier1>', create_non_terminal('<multiplier1>')),
    ('<bool_operator>', create_non_terminal('<bool_operator>')),

    ("main", create_terminal('main', 64)),
    ("int", create_terminal('int', 3)),
    ('float', create_terminal('float', 4)),
    ('ID', create_terminal('ID', 0)),
    ('CONST', create_terminal('CONST', 1)),
    ('{', create_terminal('{', 47)),
    ('}', create_terminal('}', 48)),
    (r'\n', create_terminal(r'\n', 103)),
    ('in', create_terminal('in', 85)),
    ('out', create_terminal('out', 84)),
    ('(', create_terminal('(', 45)),
    (')', create_terminal(')', 46)),
    ('if', create_terminal('if', 60)),
    ('else', create_terminal('else', 74)),
    ('=', create_terminal('=', 21)),
    ('+', create_terminal('+', 22)),
    ('-', create_terminal('-', 23)),
    ('@', create_terminal('@', 24)),
    ('*', create_terminal('*', 25)),
    ('/', create_terminal('/', 26)),
    ('%', create_terminal('%', 27)),
    ('for', create_terminal('for', 61)),
    ('to', create_terminal('to', 62)),
    ('do', create_terminal('do', 64)),
    ('<', create_terminal('<', 10)),
    ('>', create_terminal('>', 11)),
    ('<=', create_terminal('<=', 12)),
    ('>=', create_terminal('>=', 13)),
    ('!=', create_terminal('!=', 14)),
    ('==', create_terminal('==', 15)),

])


def rule_creator(token, args):
    return tuple([
        grammar_elements[token],
        tuple(tuple(grammar_elements[i] for i in rule) for rule in args)
    ])


grammar = OrderedDict(
    [
        rule_creator(token='<main>', args=[['main', '<block>']]),
        rule_creator(token='<data_type>', args=[['int'],
                                                ['float']]),
        rule_creator(token='<param_list>', args=[['<value>']]),
        rule_creator(token='<variable>', args=[['<data_type>', '<value>']]),
        rule_creator(token='<block>', args=[['{', '<block_body>', '}']]),
        rule_creator(token='<block_body>', args=[['<block_body1>']]),
        rule_creator(token='<block_body1>', args=[['<source_code_string>'],
                                                  ['<source_code_string>', '<block_body1>']]),
        rule_creator(token='<source_code_string>', args=[['<sc_element>', r'\n'],
                                                         [r'\n']]),
        rule_creator(token='<sc_element>', args=[['<variable>'],
                                                 ['<inp>'],
                                                 ['<out>'],
                                                 ['<for_cycle>'],
                                                 ['<if_expression>'],
                                                 ['<arithmetic_expression>']]),
        rule_creator(token='<inp>', args=[['in', '(', '<param_list>', ')']]),
        rule_creator(token='<out>', args=[['out', '(', '<param_list>', ')']]),
        rule_creator(token='<if_expression>', args=[['if', '(', '<bool_expression>', ')', '<block>'],
                                                    ['if', '(', '<bool_expression>', ')', '<block>', 'else', '<block>']]),
        rule_creator(token='<arithmetic_expression>', args=[['ID', '=', '<arithmetic_expression_body2>']]),
        rule_creator(token='<arithmetic_expression_body2>', args=[['<arithmetic_expression_body1>']]),
        rule_creator(token='<arithmetic_expression_body1>', args=[['<arithmetic_expression_body>']]),
        rule_creator(token='<arithmetic_expression_body>', args=[['<term1>'],
                                                                 ['<arithmetic_expression_body>', '+', '<term1>'],
                                                                 ['<arithmetic_expression_body>', '-', '<term1>'],
                                                                 ['@', '<term1>']]),
        rule_creator(token='<term1>', args=[['<term>']]),
        rule_creator(token='<term>', args=[['<multiplier1>'],
                                           ['<term>', '*', '<multiplier1>'],
                                           ['<term>', '/', '<multiplier1>'],
                                           ['<term>', '%', '<multiplier1>']]),
        rule_creator(token='<multiplier1>', args=[['<value>'],
                                                  ['<multiplier>']]),
        rule_creator(token='<multiplier>', args=[['(', '<arithmetic_expression_body2>', ')']]),
        rule_creator(token='<value>', args=[['ID'],
                                            ['CONST']]),
        rule_creator(token='<for_cycle>', args=[
            ['for', '<arithmetic_expression>', 'to', '<arithmetic_expression_body2>', 'do', '<block>']]),
        rule_creator(token='<bool_expression>', args=[['<value>', '<bool_operator>', '<value>']]),
        rule_creator(token='<bool_operator>', args=[['<'],
                                                    ['>'],
                                                    ['<='],
                                                    ['>='],
                                                    ['!='],
                                                    ['==']])
    ]
)


if __name__ == '__main__':
    for i in grammar:
        print('{!s:10}: {!s}'.format(i.name, [[k.name for k in j] for j in grammar[i]]))
