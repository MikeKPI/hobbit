class AlphabetClass:
    data_types = {
        'int':      3,
        'float':    4
    }
    splitters = {
        '<':        10,
        '>':        11,
        '<=':       12,
        '>=':       13,
        '!=':       14,
        '==':       15,
        '=':        21,
        '+':        22,
        '-':        23,
        '@': 24,
        '*': 25,
        '/': 26,
        '%': 27,
        '(':        45,
        ')':        46,
        '{':        47,
        '}':        48,
        ',':        52,
        '"':        54,
        ';':        55,
        '#':        102,
        r'\n':      103,
    }
    key_words = {
        'if':       60,
        'for':      61,
        'to':       62,
        'do':       63,
        'main':     64,
        'else':     74,
        'return':   79,
        'out':   84,
        'in':    85,
    }

    def isDataType(self, checkable):
        """
        checks is the checkable is a data type
        :returns True if checkable is Data Type, otherwise - False
        """
        try:
            self.data_types[checkable.name]          # tries to get a code for checkable in data_type dictionary
            return True                         # if it can't to get it checkable isn't a data type
        except KeyError:                        # otherwise - is Data Type
            return False

    def isReserved(self, checkable):
        """
        checks is the checkable is a reserved word
        :returns True if it's a reserved word, otherwise - False
        """
        try:                                    # tries to get a code of data type for checkable
            self.data_types[checkable.name]
            return True
        except KeyError:
            try:
                self.splitters[checkable.name]       # tries to get a code of splitter for checkable
                return True
            except KeyError:
                try:
                    self.key_words[checkable.name]   # tries to get a code of key word for checkable
                    return True
                except KeyError:                # if it can get one of the codes it returns true
                    return False                # otherwise it returns false

    def getCode(self, var):
        """
        try to get a code of variable
        :returns if it's an alphabet key it returns code, otherwise - 0
        """
        if var in self.splitters:
            return self.splitters[var]
        elif var in self.data_types:
            return self.data_types[var]
        elif var in self.key_words:
            return self.key_words[var]
        else:
            return 0

Alphabet = AlphabetClass()
