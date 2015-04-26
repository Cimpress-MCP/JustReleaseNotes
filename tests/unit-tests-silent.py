import unittest
import sys

if __name__ == '__main__':
    try:
        test_loader = unittest.defaultTestLoader
        test_suite = test_loader.discover("tests", pattern='*_Test.py')
        res = unittest.TestResult()
        test_suite.run(res)
        if not test_suite.wasSuccessful():
            sys.exit(1)
    except:
        sys.exit(1)
