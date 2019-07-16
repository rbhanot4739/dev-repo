class Player:
    def __init__(self, name):
        self.name = name
        self._level = 1
        self._lives = 3
        self._score = 0

    def _get_lives_(self):
        return self._lives

    def _set_lives_(self, lives):
        if self._lives >= 0:
            self._lives = lives

    def _get_level_(self):
        return self._level

    def _set_level_(self, level):
        if level > 0:
            self._level = level
            self._score = (level * 1000) - 1000
        else:
            print("Level can't be less than 1 !!")

    lives = property(fget=_get_lives_, fset=_set_lives_)
    level = property(_get_level_, _set_level_)

    def __str__(self):
        return 'Name: {0.name}, Score: {0._score}, Level: {0.level}, Lives: {0.lives}'.format(self)


if __name__ == '__main__':
    rb = Player('rb')
    print(rb)
    rb.level = 2
    print(rb)
    rb.level = 5
    print(rb)
    rb.level = 10
    print(rb)
    rb.level = 0
