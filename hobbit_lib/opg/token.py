from tokenizer import token


class Token(token.Token):
    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        t = hash((self.name,))
        return t
