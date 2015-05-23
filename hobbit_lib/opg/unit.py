class Unit:
    LASTS = 0
    FIRSTS = 1

    def __init__(self, token):
        self.token = token
        self.lasts = set()
        self.firsts = set()
        self.equals = set()
        self.name = token.name

    def buildPlus(self, type: int):
        operable = self.lasts if type == self.LASTS else self.firsts
        position = 0
        while position < len(operable):
            tmp_position = len(operable)
            tmp_lasts = list(operable)
            for i in range(position, len(operable)):
                self.lasts |= set(tmp_lasts[i].lasts)
            position = tmp_position

    def __str__(self):
        return '---------------------\n' \
               '{name}' \
               '\tfirsts: {firsts}\n' \
               '\tlasts: {lasts}\n' \
               '\tequals: {equals}\n' \
               '---------------------\n'\
            .format(name=self.token,
                    firsts=[i.name for i in self.firsts],
                    lasts=[i.name for i in self.lasts],
                    equals=[i.name for i in self.equals])


if __name__ == '__main__':
    a = Unit('a')
    b = Unit('b')
    c = Unit('c')
    a.lasts = {b, c}
    b.lasts = {a, c, b}
    c.lasts = {}
    c.buildPlus(Unit.LASTS)
    for i in c.lasts:
        print(i)
