class Unit:
    LASTS = 0
    FIRSTS = 1

    def __init__(self, token: str):
        self.token = token
        self.lasts = {}
        self.firsts = {}

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
        return '{name}'.format(name=self.token)


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
