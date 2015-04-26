import unittest
import sys

if __name__ == '__main__':
    try:
        test_loader = unittest.defaultTestLoader
        test_runner = unittest.TextTestRunner()
        test_suite = test_loader.discover("tests", pattern='*_Test.py')
        test_runner.run(test_suite)
    except:
        sys.exit(1)
