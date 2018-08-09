#!/usr/bin/env python

from argparse import ArgumentParser
from src.tm.tm import TuringMachine
from src.parser.llkparser import parse
from src.exception.exception import ParserException

def main(path, tm_input, debug, accept, printable) :
    src = readFile(path)
    tm = assembleTM(src)
    if printable :
        return str(tm)
    elif accept :
        return tm.accept(tm_input, debug = debug)
    else :
        return tm.run(tm_input, debug = debug)

def readFile(path) :
    try :
        file = open(path)
    except IOError as e :
        raise ParserException(e)
    return file.read()

def assembleTM(src) :
    tm = TuringMachine()
    for dec in parse(src) :
        if len(dec['inStates']) == len(dec['inSymbols']) == 0 :
            tm.setStartState(dec['outStates'].pop())
        elif len(dec['outStates']) == len(dec['outSymbols']) == len(dec['movement']) == 0 :
            tm.addAcceptStates(dec['inStates'])
        else :
            tm.addTransition(**dec)
    return tm

def parseArgs() :
    argparser = ArgumentParser(description = 'Command line utility for TMscript')
    argparser.add_argument('path', help = 'path to the source file to execute')
    argparser.add_argument('input', help = 'input string, or initial symbols on the tape', nargs = '?', default = '')
    argparser.add_argument('-d', '--debug', help = 'show debug information during the execution', action = 'store_true')
    group = argparser.add_mutually_exclusive_group()
    group.add_argument('-a', '--accept', help = 'return 1 if the Turing machine accepted the input, 0 otherwise', action = 'store_true')
    group.add_argument('-p', '--printable', help = 'only print the Turing machine tupel without running it', action = 'store_true')
    args = argparser.parse_args()
    return args.path, args.input, args.debug, args.accept, args.printable

if __name__ == '__main__' :
    args = parseArgs()
    out = main(*args)
    print out
