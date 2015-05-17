"""
Set of exceptions that I used in my tokenizer.
"""


class OverriddenException(Exception):
    def __init__(self, lnumber):
        self._line_number = lnumber

    def __str__(self):
        return repr(format("In line %d you have an error: token cannot be overridden" %
                           self._line_number))

class UnknownVariableException(Exception):
    def __init__(self, lnumber):
        self._line_number = lnumber

    def __str__(self):
        return repr(format("In line %d you have an error: unknown variable") %
                           self._line_number)


class SymbolNotFoundException(Exception):
    def __init__(self, lnumber):
        self._line_number = lnumber

    def __str__(self):
        return repr(format("In line %d you have an error: symbol not found")%self._line_number)


class InvalidRecordOfFloatNumberException(Exception):
    def __init__(self, lnumber):
        self._line_number = lnumber

    def __str__(self):
        return repr(format("In line %d you have an error: invalid record of float number" %
                    self._line_number))


class UnexpectedSymbolException(Exception):
    def __init__(self, lnumber):
        self._line_number = lnumber

    def __str__(self):
        return repr(format("In line %d you have an error: unexpected symbol" % self._line_number))


class WrongStringVariableEndException(Exception):
    def __init__(self, lnumber):
        self._line_number = lnumber

    def __str__(self):
        return repr(format("In line %d you have an error: string must be ended at the same line by using symbol \" " %
                    self._line_number))


class EmptyLineReadingException(Exception):
    def __init__(self, lnumber):
        self._line_number = lnumber

    def __str__(self):
        return repr(format("In line %d you have an error: line already ends" % self._line_number))