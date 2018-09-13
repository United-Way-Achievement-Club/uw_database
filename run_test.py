#!/usr/bin/env python2.7
from app.test.utils_test import *
import unittest

def suite():
    suite = unittest.TestSuite()
    suite.addTest(Utils('testValidateMemberException'))
    suite.addTest(Utils('testValidateMemberInvalid'))
    suite.addTest(Utils('testValidateMemberValid'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())