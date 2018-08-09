#!/usr/bin/env python

from test import Test
from src.parser.llkparser import parse
from src.token.token import ControlToken, IdentToken, StringToken
from src.tm.tm import TuringMachine
from src.exception.exception import TmException

def _assembleTM(src) :
    tm = TuringMachine()
    for dec in parse(src) :
        if len(dec['inStates']) == len(dec['inSymbols']) == 0 :
            assert len(dec['outStates']) == 1
            tm.setStartState(dec['outStates'].pop())
        elif len(dec['outStates']) == len(dec['outSymbols']) == len(dec['movement']) == 0 :
            tm.addAcceptStates(dec['inStates'])
        else :
            tm.addTransition(**dec)
    return tm

@Test
def simpleTest() :
    src = '''
    () -> (q)
    '''
    tm = _assembleTM(src)
    assert len(tm.states) == 1
    assert len(tm.alphabet) == 0
    assert tm.startState is not None
    assert len(tm.acceptStates) == 0
    s = 'Hello World!'
    assert tm.run(s) == s
    assert not tm.accept(s)

@Test
def skipperTest() :
    src = '''
    () -> (q0)
    (q0, {"0", "1"}) -> (R)
    (q0, _) -> (qf)
    (qf) -> ()
    '''
    tm = _assembleTM(src)
    assert len(tm.states) == 2
    assert len(tm.alphabet) == 2
    assert tm.startState is not None
    assert len(tm.acceptStates) == 1
    s = "01000101001101"
    assert tm.run(s) == s
    assert tm.accept(s)

@Test
def inverterTest() :
    src = '''
    # Invert a sequence of 0s and 1s
    () -> (q0)
    (q0, "0") -> ("1", R)
    (q0, "1") -> ("0", R)
    (q0, _) -> (qf)
    (qf) -> ()
    '''
    tm = _assembleTM(src)
    assert len(tm.states) == 2
    assert len(tm.alphabet) == 2
    assert tm.startState is not None
    assert len(tm.acceptStates) == 1
    s = "01000101001101"
    assert tm.run(s) == "10111010110010"
    assert tm.accept(s)

@Test
def not10Test() :
    src = '''
    # Accepts all words without the sequence "10"
    () -> (q0)
    (q0, "0") -> (R)
    (q0, "1") -> (q1, R)
    (q1, "1") -> (q1, R)
    (_) -> (qf)
    (qf) -> ()
    '''
    tm = _assembleTM(src)
    assert len(tm.states) == 3
    assert len(tm.alphabet) == 2
    assert tm.startState is not None
    assert len(tm.acceptStates) == 1
    s = "00000111"
    assert tm.accept(s)
    s = "11111011"
    assert not tm.accept(s)

@Test
def noStartStateTest() :
    src = '''
    (q0, "0") -> ("1", R)
    (q0, "1") -> ("0", R)
    (q0, _) -> (qf)
    '''
    tm = _assembleTM(src)
    s = "000000000"
    try :
        tm.run(s)
    except TmException :
        return
    assert 0 == 1
