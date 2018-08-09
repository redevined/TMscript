#!/usr/bin/env python

from test import Test
from src.parser.llkparser import parse
from src.parser.token import ControlToken, IdentToken, StringToken

@Test
def exampleTest() :
    src = '''
    # This is an example declaration
    ({q0, q1}, "a") -> (q1, "b", R)
    '''
    declarations = parse(src)
    assert len(declarations) == 1
    dec = declarations[0]
    assert dec['inStates'] == {IdentToken('q0'), IdentToken('q1')}
    assert dec['inSymbols'] == {StringToken('a')}
    assert dec['outStates'] == {IdentToken('q1')}
    assert dec['outSymbols'] == {StringToken('b')}
    assert dec['movement'] == {IdentToken('R')}

@Test
def shortenedDeclarationsTest() :
    src = '''
    () -> (q)
    (q) -> ()
    (q) -> (q, "a", N)
    ("a") -> (q, "a", N)
    (q, "a") -> (q, "a")
    (q, "a") -> (q, N)
    (q, "a") -> ("a", N)
    (q, "a") -> (q)
    (q, "a") -> ("a")
    (q, "a") -> (N)
    '''
    declarations = parse(src)
    for dec in declarations :
        for key in ('inStates', 'inSymbols', 'outStates', 'outSymbols', 'movement') :
            assert dec.has_key(key)

@Test
def setDeclarationsTest() :
    src = '({q0, q1}, {"a0", "a1", "a2"}) -> ({q2}, {"b0", "b1", "b0"}, {L, N, R})'
    dec = parse(src)[0]
    assert len(dec['inStates']) == 2
    assert len(dec['inSymbols']) == 3
    assert len(dec['outStates']) == 1
    assert len(dec['outSymbols']) == 2
    assert len(dec['movement']) == 3

@Test
def blankDeclarationTest() :
    src = '(q, _) -> (q, _, N)'
    dec = parse(src)[0]
    assert dec['inSymbols'] == dec['outSymbols'] == {IdentToken('_')}

@Test
def epsDeclarationTest() :
    src = '(q, eps) -> (q, _, N)'
    dec = parse(src)[0]
    assert dec['inSymbols'] == {IdentToken('eps')}
