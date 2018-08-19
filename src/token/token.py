#!/usr/bin/env python

# Base token class
class Token(str) :

    def setLineNumber(self, line) :
        self.line = line

    def getLineNumber(self) :
        return self.line if hasattr(self, 'line') else None

    def __repr__(self) :
        return '{}(\'{}\')'.format(self.__class__.__name__, str(self))

# Parentheses, Braces, Comma, etc.
class ControlToken(Token) :

    def __eq__(self, other) :
        return isinstance(other, ControlToken) and str(self) == str(other)

    def __ne__(self, other) :
        return not self.__eq__(other)

# Identifier
class IdentToken(Token) :

    def __eq__(self, other) :
        return isinstance(other, IdentToken) and str(self) == str(other)

    def __ne__(self, other) :
        return not self.__eq__(other)

# String literals
class StringToken(Token) :
    pass

# Token constants
BLANK_TOKEN = IdentToken('_')
EPS_TOKEN = IdentToken('eps')
L_TOKEN = IdentToken('L')
N_TOKEN = IdentToken('N')
R_TOKEN = IdentToken('R')
