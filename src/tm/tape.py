#!/usr/bin/env python

from src.token.token import BLANK_TOKEN, L_TOKEN, R_TOKEN

# Infinite tape representing memory
class Tape(object) :

    def __init__(self, symbols) :
        self.symbols = list(symbols) if symbols else [BLANK_TOKEN]
        self.pos = 0

    # Get symbol at current position
    def read(self) :
        return self.symbols[self.pos]

    # Overwrite symbol at current position
    def write(self, symbol) :
        self.symbols[self.pos] = symbol

    # Move head left or right
    def move(self, direction) :
        if direction == L_TOKEN :
            if self.pos == 0 :
                self.symbols.insert(0, BLANK_TOKEN)
            else :
                self.pos -= 1
        elif direction == R_TOKEN :
            if self.pos == len(self.symbols) - 1 :
                self.symbols.append(BLANK_TOKEN)
            self.pos += 1

    def __str__(self) :
        return ''.join(str(a) for a in self.symbols if a != BLANK_TOKEN)

    def __iter__(self) :
        for symbol in self.symbols :
            yield symbol
