import unittest
import sys
import JustReleaseNotes

if __name__ == '__main__':
    test_loader = unittest.defaultTestLoader
    test_runner = unittest.TextTestRunner()
    test_suite = test_loader.discover("tests", pattern='*_Test.py')
    test_runner.run(test_suite)
