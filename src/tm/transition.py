#!/usr/bin/env python

from tape import EPS
from src.exception.exception import TmException

# Function for state transitions
class TransitionFunction(object) :

    def __init__(self) :
        self.index = dict()

    # Index transition by input states and symbol
    def add(self, inStates, inSymbols, *out) :
        # Set states or symbols to universal by setting them to None
        if len(inStates) == 0 :
            inStates = {None}
        elif len(inSymbols) == 0 :
            inSymbols = {None}
        # Update index tree for any state/symbol combination
        for (state, symbol) in _cartesian(inStates, inSymbols) :
            if not self.index.has_key(state) :
                self.index[state] = dict()
            if not self.index[state].has_key(symbol) :
                self.index[state][symbol] = Transition()
            self.index[state][symbol].update(*out)

    def __call__(self, state, symbol) :
        result = set()
        for (q, a) in _cartesian({state, None}, {symbol, None}) :
            if self.index.has_key(q) and self.index[q].has_key(a) :
                result.update(self.index[q][a]())
        # Include epsilon transitions
        try :
            result = self._epsClosure(result)
        except RuntimeError as e :
            raise TmException(e)
        return result

    def _epsClosure(self, result) :
        # All possible states for epsilon transitions
        resultStates = {q for (q, a, m) in result}
        for q in resultStates :
            # Update result with the epsilon closure of epsilon transition results
            if self.index.has_key(q) and self.index[q].has_key(EPS) :
                result.update(
                    self._epsClosure(
                        self.index[q][EPS]()))
        return result

    def __repr__(self) :
        return '\n'.join(
            '({}, {}) -> ({})'.format(q, a, t)
                for (q, d) in self.index.items()
                    for (a, t) in d.items())

# Transition between states
class Transition(object) :

    def __init__(self) :
        self.states = set()
        self.symbols = set()
        self.movement = set()

    # Add additional states and symbols to the transition output
    def update(self, states, symbols, movement) :
        self.states.update(states)
        self.symbols.update(symbols)
        self.movement.update(movement)

    def __call__(self) :
        outStates = self.states if len(self.states) > 0 else {None}
        outSymbols = self.symbols if len(self.symbols) > 0 else {None}
        movement = self.movement if len(self.movement) > 0 else {None}
        return _cartesian(outStates, outSymbols, movement)

    def __repr__(self) :
        return ', '.join(map(_setFormat, (self.states, self.symbols, self.movement)))

# Calculate the cartesian product of multiple sets
def _cartesian(*sets) :
    assert len(sets) >= 2
    a, sets = {(x,) for x in sets[0]}, sets[1:]
    while len(sets) > 0 :
        b, sets = sets[0], sets[1:]
        a = {x + (y,) for x in a for y in b}
    return a

# Pretty print an iterable as a set
def _setFormat(s) :
    return '{' + ', '.join(map(str, s)) + '}'
