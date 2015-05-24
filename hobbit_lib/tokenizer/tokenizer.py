from hobbit_lib.tokenizer.common.alphabet import Alphabet
from hobbit_lib.tokenizer.common.error import OverriddenException
from hobbit_lib.tokenizer.common.error import UnknownVariableException
from hobbit_lib.tokenizer.linetokenizer import LineTokenizer


class Tokenizer:
    source_to_analyze = None
    variables = []
    constants = []

    def __init__(self, source_to_analyze):
        self.source_to_analyze = source_to_analyze

    def analyze(self):
        """
        method is analyzing given file for lexical problems
        :returns dictionary of sets tokens, variables and constants
        """
        line_number = 0
        answer = []                                                         # set of all tokens
        variable_id = 0                                                     # variable used for numbering of tokens
        constant_id = 0                                                     # variable used for numbering of constants
        new_variable_create_flag = False                                    # indicate process of creating new variable
        for line in self.source_to_analyze:
            linetokenizer = LineTokenizer(line=line,
                                          line_number=line_number)
            line_number += 1
            while linetokenizer.hasNext():
                try:
                    tokens = linetokenizer.next()                           # getting next token if it exist
                    for token in tokens:
                        answer.append(token)                                # adding token to tokens list
                        token.language_id = Alphabet.getCode(token.name_value)         # getting alphabet code of toekn
                        if token.type != '':                                # checking is token is a constant
                            if not self._isConstant(token):
                                token.constant_id = constant_id             # and adding to constant list
                                constant_id += 1
                                token.name = 'CONST'
                                self.constants.append(token)
                            else:
                                token.constant_id = self.constants.index(token)
                                token.name = 'CONST'
                            token.value = token.name
                            continue
                        elif Alphabet.isDataType(token):                    # checking for start of process of creating
                            new_variable_create_flag = True                 # new variable
                            continue
                        elif new_variable_create_flag:                      # if we in process of creating new variable
                            if not Alphabet.isReserved(token):              # and token isn't reserved
                                token.variable_id = variable_id
                                variable_id += 1
                                self.variables.append(token)                # adding token to variable list
                                new_variable_create_flag = False            # end exit process of creating new variable
                                continue
                            else:
                                raise OverriddenException(lnumber=line_number)
                        elif self._isVariable(token):
                            token.variable_id = self.variables.index(token)
                            continue
                        elif not Alphabet.isReserved(token) and \
                                not self._isVariable(token) and \
                                not self._isConstant(token):                        # if token reserved
                            raise UnknownVariableException(lnumber=line_number)     # we raise an Exception

                except Exception as e:                                      # catching and printing any exception
                    raise e
        return {
            'tokens':       answer,
            'variables':    self.variables,
            'constants':    self.constants
        }

    def _isVariable(self, checkable):
        """
        inner method to check is checkable is already a variable
        :returns True if it's a variable, otherwise - False
        """
        return checkable in self.variables

    def _isConstant(self, checkable):
        """
        inner method to check is checkable is already a constant
        :returns True if it's a constant, otherwise - False
        """
        return checkable in self.constants

if __name__ == '__main__':
    import json
    with open('/Users/mike/input.hobbit') as ifile:
        tokenizer = Tokenizer(source_to_analyze=ifile)
        try:
            out = tokenizer.analyze()
            print('tokens')
            for i in out['tokens']:
                print(i)
            print('variables')
            for i in out['variables']:
                print(i)
            print('constants')
            for i in out['constants']:
                print(i)
            output_json = json.dumps({
                'tokens':       [i.toDict() for i in out['tokens']],
                'variables':    [i.toDict() for i in out['variables']],
                'constants':    [i.toDict() for i in out['constants']],
            })
            with open('/Users/mike/lolkappc', 'w') as output_js:
                output_js.write(output_json)
        except OverriddenException as oe:
            print(oe)
        except UnknownVariableException as uve:
            print(uve)
