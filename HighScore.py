class HighScore:
    def __init__(self, inits, score):
        self.initials = inits
        self.score = score

    def __eq__(self, other):
        return self.score == other.score
    def __lt__(self, other):
        if self.score == other.score:
            return self.initials < other.initials
        else:
            return self.score < other.score
    def __gt__(self, other):
        if self.score == other.score:
            return self.initials > other.initials
        else:
            return self.score > other.score
    def __str__(self):
        return self.initials + ' ' + str(self.score)

    '''
    s1 = HighScore('JPC', 76)
    s2 = HighScore('KVC', 79)
    if s1 == s2:
        print('s1 and s2 are equal')
    '''