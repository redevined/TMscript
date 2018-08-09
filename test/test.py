#!/usr/bin/env python

# Test decorator
def Test(testFunction) :
    print '> Running test {}...'.format(testFunction.func_name)
    testFunction()
    print 'Done.\n'
