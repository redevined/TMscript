#!/usr/bin/env python

from test import Test
from src.token.tokenizer import tokenize
from src.token.token import ControlToken, IdentToken, StringToken
from src.exception.exception import ParserException

@Test
def whitespaceTest() :
    src = '   \n \n\n    \t   \n\t   '
    tokens = tokenize(src)
    assert len(tokens) == 0

@Test
def lineCommentTest() :
    src = '# ## # ## (hello, "W") -> (o, 'r', L), d\n'
    tokens = tokenize(src)
    assert len(tokens) == 0

@Test
def blockCommentTest() :
    src = '### (}{) stuff\n more "stuff"\n\n () ###'
    tokens = tokenize(src)
    assert len(tokens) == 0

@Test
def identTest() :
    src = 'q0 q1q2 q'
    tokens = tokenize(src)
    assert len(tokens) == 3
    for token in tokens :
        assert isinstance(token, IdentToken)

@Test
def stringTest() :
    src = '"hello" "\\" my" "world ###"'
    tokens = tokenize(src)
    assert len(tokens) == 3
    for token in tokens :
        assert isinstance(token, StringToken)

@Test
def controlTest() :
    src = '( } , -> ) {'
    tokens = tokenize(src)
    assert len(tokens) == 6
    for token in tokens :
        assert isinstance(token, ControlToken)

@Test
def invalidIdentTest() :
    src = '0xef'
    try :
        tokenize(src)
    except ParserException :
        return
    assert 0 == 1

@Test
def exampleDeclarationTest() :
    src = '''
    # This is an example declaration
    ({q0, q1}, "a") -> (q1, "b", R)
    '''
    tokens = tokenize(src)
    assert len([t for t in tokens if isinstance(t, ControlToken)]) == 11
    assert len([t for t in tokens if isinstance(t, IdentToken)]) == 4
    assert len([t for t in tokens if isinstance(t, StringToken)]) == 2
