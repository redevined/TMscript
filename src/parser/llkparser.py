#!/usr/bin/env python

from src.token.tokenizer import tokenize
from src.token.token import ControlToken, IdentToken, StringToken, BLANK_TOKEN, EPS_TOKEN, L_TOKEN, N_TOKEN, R_TOKEN
from src.exception.exception import ParserException

# TODO don't allow eps on right side of a declaration
# TODO better parser error messages

# Parse given source code into a list of declarations (as dictionaries)
def parse(src) :
    tokens = tokenize(src)
    success, unparsed, declarations = parseDeclarations(tokens)
    if not success :
        raise ParserException('not a declaration')
    return declarations

# Decs ::= Dec Decs | empty
def parseDeclarations(tokens) :
    found, unparsed, parsedDec = parseDeclaration(tokens)
    if found :
        found, unparsed, parsedDecs = parseDeclarations(unparsed)
        if found :
            return True, unparsed, parsedDecs + [parsedDec]
    return len(tokens) == 0, tokens, list()

# Dec ::= StartDec | EndDec | ( In ) -> ( Out )
def parseDeclaration(tokens) :
    found, unparsed, dec = parseStartDeclaration(tokens)
    if found :
        return True, unparsed, dec
    found, unparsed, dec = parseEndDeclaration(tokens)
    if found :
        return True, unparsed, dec
    found, unparsed = parseControlToken(tokens, '(')
    if not found :
        return False, tokens, dict()
    found, unparsed, parsedInStates, parsedInSymbols = parseStatesSymbols(unparsed)
    if not found :
        return False, tokens, dict()
    found, unparsed = parseControlToken(unparsed, ')')
    if not found :
        return False, tokens, dict()
    found, unparsed = parseControlToken(unparsed, '->')
    if not found :
        return False, tokens, dict()
    found, unparsed = parseControlToken(unparsed, '(')
    if not found :
        return False, tokens, dict()
    found, unparsed, parsedOutStates, parsedOutSymbols, parsedMovement = parseStatesSymbolsMovement(unparsed)
    if not found :
        return False, tokens, dict()
    found, unparsed = parseControlToken(unparsed, ')')
    if not found :
        return False, tokens, dict()
    return True, unparsed, {
        'inStates': parsedInStates,
        'inSymbols': parsedInSymbols,
        'outStates': parsedOutStates,
        'outSymbols': parsedOutSymbols,
        'movement': parsedMovement
    }

# StartDec ::= ( ) -> ( State )
def parseStartDeclaration(tokens) :
    found, unparsed = parseControlToken(tokens, '(')
    if not found :
        return False, tokens, dict()
    found, unparsed = parseControlToken(unparsed, ')')
    if not found :
        return False, tokens, dict()
    found, unparsed = parseControlToken(unparsed, '->')
    if not found :
        return False, tokens, dict()
    found, unparsed = parseControlToken(unparsed, '(')
    if not found :
        return False, tokens, dict()
    found, unparsed, parsedState = parseState(unparsed)
    if not found :
        return False, tokens, dict()
    found, unparsed = parseControlToken(unparsed, ')')
    if not found :
        return False, tokens, dict()
    return True, unparsed, {
        'inStates': set(),
        'inSymbols': set(),
        'outStates': {parsedState},
        'outSymbols': set(),
        'movement': set()
    }

# EndDec ::= ( States ) -> ( )
def parseEndDeclaration(tokens) :
    found, unparsed = parseControlToken(tokens, '(')
    if not found :
        return False, tokens, dict()
    found, unparsed, parsedStates = parseStateSet(unparsed)
    if not found :
        return False, tokens, dict()
    found, unparsed = parseControlToken(unparsed, ')')
    if not found :
        return False, tokens, dict()
    found, unparsed = parseControlToken(unparsed, '->')
    if not found :
        return False, tokens, dict()
    found, unparsed = parseControlToken(unparsed, '(')
    if not found :
        return False, tokens, dict()
    found, unparsed = parseControlToken(unparsed, ')')
    if not found :
        return False, tokens, dict()
    return True, unparsed, {
        'inStates': parsedStates,
        'inSymbols': set(),
        'outStates': set(),
        'outSymbols': set(),
        'movement': set()
    }

# SS ::= States , Symbols | States | Symbols
def parseStatesSymbols(tokens) :
    # Parse states
    found, unparsed_ws, parsedStates = parseStateSet(tokens)
    if found :
        found, unparsed = parseControlToken(unparsed_ws, ',')
        if found :
            # Parse symbols
            found, unparsed, parsedSymbols = parseSymbolSet(unparsed)
            if found :
                return True, unparsed, parsedStates, parsedSymbols
        return True, unparsed_ws, parsedStates, set()
    # Parse symbols w/o states
    found, unparsed, parsedSymbols = parseSymbolSet(tokens)
    if found :
        return True, unparsed, set(), parsedSymbols
    return False, tokens, set(), set()

# SSM ::= SS , Movements | SS | Movements
def parseStatesSymbolsMovement(tokens) :
    # Parse states and symbols
    found, unparsed_ws, parsedStates, parsedSymbols = parseStatesSymbols(tokens)
    # Assert that eps is not in symbols
    if found and EPS_TOKEN not in parsedSymbols :
        found, unparsed = parseControlToken(unparsed_ws, ',')
        if found :
            # Parse movements
            found, unparsed, parsedMovements = parseMovementSet(unparsed)
            if found :
                return True, unparsed, parsedStates, parsedSymbols, parsedMovements
        return True, unparsed_ws, parsedStates, parsedSymbols, set()
    # Parse movements w/o states and symbols
    found, unparsed, parsedMovements = parseMovementSet(tokens)
    if found :
        return True, unparsed, set(), set(), parsedMovements
    return False, tokens, set(), set(), set()

# States ::= State | { State AddStates }
def parseStateSet(tokens) :
    return _parseXSet(tokens, parseState)

# Symbols ::= Symbol | { Symbol AddSymbols }
def parseSymbolSet(tokens) :
    return _parseXSet(tokens, parseSymbol)

# Movements ::= Movement | { Movement AddMovements }
def parseMovementSet(tokens) :
    return _parseXSet(tokens, parseMovement)

# State
def parseState(tokens) :
    if len(tokens) > 0 :
        token = tokens[0]
        if isinstance(token, IdentToken) and token not in (BLANK_TOKEN, EPS_TOKEN, L_TOKEN, N_TOKEN, R_TOKEN) :
            return True, tokens[1:], token
    return False, tokens, None

# Symbol
def parseSymbol(tokens) :
    if len(tokens) > 0 :
        token = tokens[0]
        if isinstance(token, StringToken) or token in (BLANK_TOKEN, EPS_TOKEN) :
            return True, tokens[1:], token
    return False, tokens, None

# Movement
def parseMovement(tokens) :
    if len(tokens) > 0 :
        token = tokens[0]
        if token in (L_TOKEN, N_TOKEN, R_TOKEN) :
            return True, tokens[1:], token
    return False, tokens, None

# ( | ) | { | } | , | ->
def parseControlToken(tokens, char) :
    if len(tokens) > 0 :
        token = tokens[0]
        if token == ControlToken(char) :
            return True, tokens[1:]
    return False, tokens

# States ::= State | { State AddStates }
# Symbols ::= Symbol | { Symbol AddSymbols }
# Movements ::= Movement | { Movement AddMovements }
def _parseXSet(tokens, parseX) :
    found, unparsed, parsedX = parseX(tokens)
    if found :
        return True, unparsed, {parsedX}
    found, unparsed = parseControlToken(tokens, '{')
    if found :
        found, unparsed, parsedX = parseX(unparsed)
        if found :
            found, unparsed, parsedXSet = _parseAdditionalX(unparsed, parseX)
            if found :
                found, unparsed = parseControlToken(unparsed, '}')
                if found :
                    return True, unparsed, {parsedX}.union(parsedXSet)
    return False, tokens, set()

# AddStates ::= , State AddStates
# AddSymbols ::= , Symbol AddSymbols
# AddMovements ::= , Movement AddMovements
def _parseAdditionalX(tokens, parseX) :
    found, unparsed = parseControlToken(tokens, ',')
    if found :
        found, unparsed, parsedX = parseX(unparsed)
        if found :
            found, unparsed, parsedXSet = _parseAdditionalX(unparsed, parseX)
            if found :
                return True, unparsed, {parsedX}.union(parsedXSet)
    return True, tokens, set()
