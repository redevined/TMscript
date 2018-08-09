#!/usr/bin/env python

from src.token.tokenizer import tokenize
from src.token.token import ControlToken, IdentToken, StringToken, BLANK_TOKEN, EPS_TOKEN, L_TOKEN, N_TOKEN, R_TOKEN
from src.exception.exception import ParserException

# TODO don't allow eps on right side of a declaration
# TODO parse start state declarations and accepting state declarations separate

# Parse given source code into a list of declarations (as dictionaries)
def parse(src) :
    tokens = tokenize(src)
    success, unparsed, declarations = _parseDeclarations(tokens)
    if not success :
        raise ParserException('not a declaration')
    return declarations

# Decs ::= Dec Decs | empty
def _parseDeclarations(tokens) :
    found, unparsed, parsedDec = _parseDeclaration(tokens)
    if found :
        found, unparsed, parsedDecs = _parseDeclarations(unparsed)
        if found :
            return True, unparsed, parsedDecs + [parsedDec]
    return len(tokens) == 0, tokens, list()

# Dec ::= ( In ) -> ( Out )
def _parseDeclaration(tokens) :
    found, unparsed = _parseControlToken(tokens, '(')
    if not found :
        return False, tokens, dict()
    found, unparsed, parsedInStates, parsedInSymbols = _parseStatesSymbols(unparsed)
    if not found :
        return False, tokens, dict()
    found, unparsed = _parseControlToken(unparsed, ')')
    if not found :
        return False, tokens, dict()
    found, unparsed = _parseControlToken(unparsed, '->')
    if not found :
        return False, tokens, dict()
    found, unparsed = _parseControlToken(unparsed, '(')
    if not found :
        return False, tokens, dict()
    found, unparsed, parsedOutStates, parsedOutSymbols, parsedMovement = _parseStatesSymbolsMovement(unparsed)
    if not found :
        return False, tokens, dict()
    found, unparsed = _parseControlToken(unparsed, ')')
    if not found :
        return False, tokens, dict()
    return True, unparsed, {
        'inStates': parsedInStates,
        'inSymbols': parsedInSymbols,
        'outStates': parsedOutStates,
        'outSymbols': parsedOutSymbols,
        'movement': parsedMovement
    }

# SS ::= States , Symbols | States | Symbols | empty
def _parseStatesSymbols(tokens) :
    found, unparsed_ws, parsedStates = _parseXSet(tokens, _parseState)
    if found :
        found, unparsed = _parseControlToken(unparsed_ws, ',')
        if found :
            found, unparsed, parsedSymbols = _parseXSet(unparsed, _parseSymbol)
            if found :
                return True, unparsed, parsedStates, parsedSymbols
        return True, unparsed_ws, parsedStates, set()
    found, unparsed, parsedSymbols = _parseXSet(tokens, _parseSymbol)
    if found :
        return True, unparsed, set(), parsedSymbols
    return True, tokens, set(), set()

# SSM ::= SS , Movements | SS | Movements | empty
def _parseStatesSymbolsMovement(tokens) :
    found, unparsed_ws, parsedStates, parsedSymbols = _parseStatesSymbols(tokens)
    # if (found):... is not viable here, because SS -> empty is possible and we want to check for movement in this case
    if parsedStates or parsedSymbols :
        found, unparsed = _parseControlToken(unparsed_ws, ',')
        if found :
            found, unparsed, parsedMovements = _parseXSet(unparsed, _parseMovement)
            if found :
                return True, unparsed, parsedStates, parsedSymbols, parsedMovements
        return True, unparsed_ws, parsedStates, parsedSymbols, set()
    found, unparsed, parsedMovements = _parseXSet(tokens, _parseMovement)
    if found :
        return True, unparsed, set(), set(), parsedMovements
    return True, tokens, set(), set(), set()

# States ::= State | { State AddStates }
# Symbols ::= Symbol | { Symbol AddSymbols }
# Movements ::= Movement | { Movement AddMovements }
def _parseXSet(tokens, _parseX) :
    found, unparsed, parsedX = _parseX(tokens)
    if found :
        return True, unparsed, {parsedX}
    found, unparsed = _parseControlToken(tokens, '{')
    if found :
        found, unparsed, parsedX = _parseX(unparsed)
        if found :
            found, unparsed, parsedXSet = _parseAdditionalX(unparsed, _parseX)
            if found :
                found, unparsed = _parseControlToken(unparsed, '}')
                if found :
                    return True, unparsed, {parsedX}.union(parsedXSet)
    return False, tokens, set()

# AddStates ::= , State AddStates
# AddSymbols ::= , Symbol AddSymbols
# AddMovements ::= , Movement AddMovements
def _parseAdditionalX(tokens, _parseX) :
    found, unparsed = _parseControlToken(tokens, ',')
    if found :
        found, unparsed, parsedX = _parseX(unparsed)
        if found :
            found, unparsed, parsedXSet = _parseAdditionalX(unparsed, _parseX)
            if found :
                return True, unparsed, {parsedX}.union(parsedXSet)
    return True, tokens, set()

# State
def _parseState(tokens) :
    if len(tokens) > 0 :
        token = tokens[0]
        if isinstance(token, IdentToken) and token not in (BLANK_TOKEN, EPS_TOKEN, L_TOKEN, N_TOKEN, R_TOKEN) :
            return True, tokens[1:], token
    return False, tokens, None

# Symbol
def _parseSymbol(tokens) :
    if len(tokens) > 0 :
        token = tokens[0]
        if isinstance(token, StringToken) or token in (BLANK_TOKEN, EPS_TOKEN) :
            return True, tokens[1:], token
    return False, tokens, None

# Movement
def _parseMovement(tokens) :
    if len(tokens) > 0 :
        token = tokens[0]
        if token in (L_TOKEN, N_TOKEN, R_TOKEN) :
            return True, tokens[1:], token
    return False, tokens, None

# ( | ) | { | } | , | ->
def _parseControlToken(tokens, char) :
    if len(tokens) > 0 :
        token = tokens[0]
        if token == ControlToken(char) :
            return True, tokens[1:]
    return False, tokens
