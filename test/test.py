#!/usr/bin/env python

from cStringIO import StringIO
import sys

# Test decorator
def Test(testFunction) :
    print '> Running test {}...'.format(testFunction.func_name)

    old_stdout = sys.stdout
    sys.stdout = debugOutput = StringIO()

    testFunction()

    sys.stdout = old_stdout
    output = debugOutput.getvalue()
    if output :
        print output

    print 'Done.\n'
