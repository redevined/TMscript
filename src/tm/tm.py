#!/usr/bin/env python

from transition import TransitionFunction
from tape import Tape
from src.token.token import BLANK_TOKEN, EPS_TOKEN
from src.exception.exception import TmException


# TM state
class State(object) :

    def __init__(self, name) :
        self.name = str(name)

    def __eq__(self, other) :
        return self.name == other.name

    def __ne__(self, other) :
        return not self.__eq__(other)

    def __hash__(self) :
        return hash(self.name)

    def __repr__(self) :
        return '({})'.format(self.name)

# Class for assembling and running the TM
class TuringMachine(object) :

    def __init__(self) :
        self.alphabet = set()
        self.states = set()
        self.startState = None
        self.acceptStates = set()
        self.transitionFunction = TransitionFunction()

    # Define new transition by their input states and symbols, and their output states, symbols and tape movement
    def addTransition(self,
            inStates = set(), inSymbols = set(),
            outStates = set(), outSymbols = set(), movement = set()) :
        self.transitionFunction.add(
            self._updateStates(inStates), self._updateAlphabet(inSymbols),
            self._updateStates(outStates), self._updateAlphabet(outSymbols), movement)

    # Assign initial state
    def setStartState(self, state) :
        state = State(state)
        self.states.add(state)
        self.startState = state

    # Define accepting (end) states
    def addAcceptStates(self, states) :
        states = _setMap(State, states)
        self.states.update(states)
        self.acceptStates.update(states)

    def _updateStates(self, states) :
        states = _setMap(State, states)
        self.states.update(states)
        return states

    def _updateAlphabet(self, symbols) :
        new_symbols = set()
        for a in symbols :
            if a == BLANK_TOKEN :
                new_symbols.add(BLANK_TOKEN)
            elif a == EPS_TOKEN :
                new_symbols.add(EPS_TOKEN)
            else :
                new_symbols.add(a)
                self.alphabet.add(a)
        return new_symbols

    # Run Turing machine on provided input, return output string
    def run(self, symbols = [], debug = False) :
        tape = Tape(symbols)
        self._run(tape, debug)
        return str(tape)

    # Run Turing machine on provided input, return true if TM accepts input
    def accept(self, symbols = [], debug = False) :
        tape = Tape(symbols)
        endState = self._run(tape, debug)
        return endState in self.acceptStates

    def _run(self, tape, debug) :
        if not isinstance(self.startState, State) :
            raise TmException('no starting state defined')
        state = self.startState
        trans = self.transitionFunction(state, tape.read())
        n = 0
        # Debug output
        if debug :
            _printDebug(tape, state, n)
        # Main execution loop
        while len(trans) > 0 and state not in self.acceptStates :
            # TODO implement non-deterministic behavior
            if len(trans) > 1 :
                raise TmException('non-deterministic behavior not yet implemented')
            # Apply transition result
            q, a, m = trans.pop()
            if q :
                state = q
            if a :
                tape.write(a)
            tape.move(m)
            # Get next transition
            trans = self.transitionFunction(state, tape.read())
            n += 1
            # Debug output
            if debug :
                _printDebug(tape, state, n)
        # Return last state
        return state

    def __repr__(self) :
        # M = (Q, Sig, delta, q0, F)
        return 'TM = (\n\tQ = {q},\n\tA = {a},\n\tt =\t{t},\n\ts = {s},\n\tF = {f}\n)'.format(
            q = _setFormat(self.states),
            a = _setFormat(self.alphabet),
            t = str(self.transitionFunction).replace('\n', '\n\t\t'),
            s = self.startState,
            f = _setFormat(self.acceptStates))

# Map function to set and return as set
def _setMap(f, s) :
    return {f(x) for x in s}

# Pretty print an iterable as a set
def _setFormat(s) :
    return '{' + ', '.join(map(str, s)) + '}'

# Debugging output
def _printDebug(tape, state, i) :
    print 'Configuration in iteration {}:'.format(i)
    print 4 * tape.pos * ' ' + str(state)
    print 4 * tape.pos * ' ' + ' V'
    print ' ' + ' | '.join(' ' if a == BLANK_TOKEN else str(a) for a in tape) + '\n'
