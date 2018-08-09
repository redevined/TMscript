#!/usr/bin/env python

from test import Test
from src.tm.tm import TuringMachine
from src.token.token import BLANK_TOKEN, EPS_TOKEN, L_TOKEN, R_TOKEN

@Test
def stupidTest() :
    tm = TuringMachine()
    assert isinstance(tm, TuringMachine)

@Test
def skipperTest() :
    tm = TuringMachine()
    tm.setStartState('q0')
    tm.addTransition(
        inSymbols = {'0', '1'},
        movement = {R_TOKEN})
    s = '0110'
    out = tm.run(s)
    assert out == s

@Test
def inverterTest() :
    tm = TuringMachine()
    tm.setStartState('q0')
    tm.addTransition(
        inStates = {'q0'}, inSymbols = {'0'},
        outSymbols = {'1'}, movement = {R_TOKEN})
    tm.addTransition(
        inStates = {'q0'}, inSymbols = {'1'},
        outSymbols = {'0'}, movement = {R_TOKEN})
    s = '0110'
    out = tm.run(s)
    assert out == '1001'

@Test
def busybeaver3Test() :
    tm = TuringMachine()
    tm.setStartState('q0')
    tm.addTransition(
        inStates = {'q0'}, inSymbols = {BLANK_TOKEN},
        outStates = {'q1'}, outSymbols = {'1'}, movement = {R_TOKEN})
    tm.addTransition(
        inStates = {'q1'}, inSymbols = {'1'},
        movement = {R_TOKEN})
    tm.addTransition(
        inStates = {'q1'}, inSymbols = {BLANK_TOKEN},
        outStates = {'q2'}, movement = {R_TOKEN})
    tm.addTransition(
        inStates = {'q2'}, inSymbols = {BLANK_TOKEN},
        outSymbols = {'1'}, movement = {L_TOKEN})
    tm.addTransition(
        inStates = {'q2'}, inSymbols = {'1'},
        outStates = {'q0'}, movement = {L_TOKEN})
    tm.addTransition(
        inStates = {'q0'}, inSymbols = {'1'},
        outStates = {'qf'})
    out = tm.run()
    assert out == '111111'

@Test
def acceptAllTest() :
    tm = TuringMachine()
    tm.setStartState('q0')
    tm.addAcceptStates({'q0'})
    out = tm.accept()
    assert out == True

@Test
def acceptNoneTest() :
    tm = TuringMachine()
    tm.setStartState('q0')
    out = tm.accept()
    assert out == False

@Test
def alternatingTest() :
    tm = TuringMachine()
    tm.setStartState('q0')
    tm.addTransition(
        inStates = {'q0'}, inSymbols = {'1'},
        outStates = {'q1'}, movement = {R_TOKEN})
    tm.addTransition(
        inStates = {'q1'}, inSymbols = {'0'},
        outStates = {'q0'}, movement = {R_TOKEN})
    tm.addTransition(
        inStates = {'q0', 'q1'}, inSymbols = {BLANK_TOKEN},
        outStates = {'qf'})
    tm.addAcceptStates({'qf'})
    s = '101010101'
    out = tm.accept(s)
    assert out == True
    s = '101001010'
    out = tm.accept(s)
    assert out == False
