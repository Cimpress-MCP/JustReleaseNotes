import unittest
import sys
import JustReleaseNotes

if __name__ == '__main__':
    test_loader = unittest.defaultTestLoader
    test_suite = test_loader.discover("tests", pattern='*_Test.py')
    res = unittest.TestResult()
    test_suite.run(res)

    if not res.wasSuccessful():
        print("Errors:")
        for tuple in res.errors:
            print(tuple)

        print("Failures:")
        for tuple in res.failures:
            print(tuple)

        sys.exit(1)

