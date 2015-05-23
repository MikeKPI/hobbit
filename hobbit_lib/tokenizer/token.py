class Token:
    type = ""
    name = ""
    line_number = 0
    language_id = 0
    variable_id = None
    constant_id = None
    value = None

    def __init__(self, name, type, line_number, language_id=0):
        self.name = name
        self.type = type
        self.line_number = line_number
        self.language_id = language_id

    @staticmethod
    def fromDict(dictionary):
        new = Token(dictionary['name'],
                    dictionary['type'],
                    dictionary['line_number'])
        new.language_id = dictionary['alphabet_id']
        new.variable_id = dictionary['variable_id']

        return new

    def __str__(self):
        """
        method represent Token in readable form
        :returns representing string
        """
        return self.name
        # return format('line: {!s:>5} \u007c token: {!s:>20} \u007c type: {!s:>6} \u007c alphabet_id: {!s:>5} '
        #               '\u007c variable_id: {!s:>5} \u007c constant_id: {!s:>5} \u007c value: {!s}'
        #               .format(self.line_number, self.name, self.type, self.language_id,
        #                       self.variable_id, self.constant_id, self.value))

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash((self.name, self.line_number))

    def toDict(self):
        """
        method represent Token in dictionary form
        :returns dictionary that can be used in creation of json object
        """
        return {
            "line_number": self.line_number,
            "name": self.name,
            "type": self.type,
            "alphabet_id": self.language_id,
            "variable_id": self.variable_id,
            "constant_id": self.constant_id,
            "value": self.value
        }
