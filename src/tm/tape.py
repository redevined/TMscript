#!/usr/bin/env python

# Tape symbol
class Symbol(object) :

    def __init__(self, char) :
        assert isinstance(char, str)
        self.char = char

    def __eq__(self, other) :
        return self.char == other.char

    def __ne__(self, other) :
        return not self.__eq__(other)

    def __hash__(self) :
        return hash(self.char)

    def __repr__(self) :
        return self.char

# Infinite tape representing memory
class Tape(object) :

    def __init__(self, symbols) :
        self.symbols = symbols if symbols else [BLANK]
        self.pos = 0

    # Get symbol at current position
    def read(self) :
        return self.symbols[self.pos]

    # Overwrite symbol at current position
    def write(self, symbol) :
        self.symbols[self.pos] = symbol

    # Move head left or right
    def move(self, direction) :
        if direction == L :
            if self.pos == 0 :
                self.symbols.insert(0, BLANK)
            else :
                self.pos -= 1
        elif direction == R :
            if self.pos == len(self.symbols) - 1 :
                self.symbols.append(BLANK)
            self.pos += 1

    def __repr__(self) :
        return ''.join(map(str, self.symbols))

    def __iter__(self) :
        for symbol in self.symbols :
            yield symbol

# Tape constants
BLANK = Symbol('')
EPS = Symbol('eps')
L = 'L'
R = 'R'
