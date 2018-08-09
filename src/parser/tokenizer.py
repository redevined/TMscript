#!/usr/bin/env python

import re
from token import ControlToken, IdentToken, StringToken
from src.exception.exception import ParserException

# Split source code into tokens while ignoring comments and whitespace
def tokenize(src) :
    tokens = list()
    pos = 0
    while pos < len(src) :
        char = src[pos]
        if char in (' ', '\t', '\n') :
            pass
        elif char == '#' :
            pos = _ignoreComment(src, pos)
        elif char in ('(', ')', '{', '}', ',') :
            tokens.append(ControlToken(char))
        elif char == '-' and src[pos + 1] == '>' :
            tokens.append(ControlToken('->'))
            pos += 1
        elif re.match(r'[A-Za-z_]', char) :
            token, pos = _tokenizeIdent(src, pos)
            tokens.append(IdentToken(token))
        elif char in ('\'', '"') :
            try :
                token, pos = _tokenizeString(src, pos)
            except IndexError :
                raise ParserException('unterminated string token')
            tokens.append(StringToken(token))
        else :
            raise ParserException('unknown token {}'.format(char))
        pos += 1
    return tokens

def _tokenizeIdent(src, pos) :
    token = ''
    while pos < len(src) and re.match(r'[A-Za-z_0-9]', src[pos])  :
        token += src[pos]
        pos += 1
    return token, pos - 1

def _tokenizeString(src, pos) :
    token = ''
    strchar = src[pos]
    pos += 1
    while src[pos] != strchar :
        token += src[pos]
        # Don't check for end of string on the next character if backslash
        if src[pos] == '\\' :
            pos += 1
            token += src[pos]
        pos += 1
    return token, pos

def _ignoreComment(src, pos) :
    isComment = lambda p : src[p] != '\n'
    # If block comment, swap break criterium
    if pos + 2 < len(src) and src[pos + 1] == src[pos + 2] == '#' :
        isComment = lambda p : not src[p] == src[p - 1] == src[p - 2] == '#'
        pos += 3
    while pos < len(src) and isComment(pos)  :
        pos += 1
    return pos
