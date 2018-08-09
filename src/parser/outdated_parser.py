#!/usr/bin/env python

from tokenizer import tokenize
from token import ControlToken, IdentToken, StringToken

### Constants

BLANK, EPS, L, N, R

### Parsing algorithm

def parse(src) :
    tokens = tokenize(src)
    _parseDeclarations(tokens)

def _parseDeclarations(tokens) :
    assert tokens[0] == ControlToken('(') # TODO use assertions? probably not
    index = tokens.find(ControlToken(')'))
    inStates, inSymbols = _parseDeclarationInput(tokens[1:index])
    assert tokens[index + 1] == ControlToken('->')

    tokens = tokens[index + 2:]
    assert tokens[0] == ControlToken('(')
    index = tokens.find(ControlToken(')'))
    outStates, outSymbols, movement = _parseDeclarationOutput(tokens[1:index])

    # TODO do something
    _parseDeclarations(tokens[index + 1:])

def _parseDeclarationInput(tokens) :
    states, symbols = _parseStates(tokens), set()
    if len(tokens) != 0 :
        assert len(states) == 0 or tokens.pop(0) == ControlToken(',')
        symbols = _parseSymbols(tokens)
    assert len(tokens) == 0
    return states, symbols

def _parseDeclarationOutput() :
    states, symbols, movement = _parseStates(tokens), set(), set()
    if len(tokens) != 0 :
        assert len(states) == 0 or tokens.pop(0) == ControlToken(',')
        symbols = _parseSymbols(tokens)
    if len(tokens) != 0 :
        assert (len(states) == 0 and len(symbols) == 0) or tokens.pop(0) == ControlToken(',')
        movement = _parseMovement(tokens)
    assert len(tokens) == 0
    return states, symbols, movement

def _parseStates(tokens) :
    token = tokens.pop(0)
    if isinstance(token, IdentToken) :
        return {token}
    elif token == ControlToken('{') :
        return _parseStateSet(tokens)
    else :
        tokens.insert(0, token)
        return set()

def _parseStateSet() :
    pass

def _parseSymbols() :
    token = tokens.pop(0)
    if isinstance(token, StringToken) :
        return {token}
    elif token == ControlToken('{') :
        return _parseSymbolSet(tokens)
    elif token == IdentToken('_') :
        return {BLANK}
    elif token == IdentToken('eps') :
        return {EPS}
    else :
        tokens.insert(0, token)
        return set()

def _parseSymbolSet() :
    pass

def _parseMovement() :
    pass
