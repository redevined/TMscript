#!/usr/bin/env python

from argparse import ArgumentParser
from src.tm.tm import TuringMachine
from src.parser.llkparser import parse

def main(path, debug, accept, printable) :
    return 0

def parseArgs() :
    argparser = ArgumentParser(description = 'Command line utility for TMscript')
    argparser.add_argument('path', help = 'path to the source file to execute')
    argparser.add_argument('-d', '--debug', help = 'show debug information during the execution', action = 'store_true')
    group = argparser.add_mutually_exclusive_group()
    group.add_argument('-a', '--accept', help = 'return 1 if the Turing machine accepted the input, 0 otherwise', action = 'store_true')
    group.add_argument('-p', '--printable', help = 'only print the Turing machine tupel without running it', action = 'store_true')
    args = argparser.parse_args()
    return args.path, args.debug, args.accept, args.printable

if __name__ == '__main__' :
    main(*parseArgs())
