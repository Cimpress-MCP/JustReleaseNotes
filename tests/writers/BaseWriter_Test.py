import unittest
from JustReleaseNotes.writers import BaseWriter
import sys

class BaseWriter_Test(unittest.TestCase):
    def test_convertVersionTranslatesMaxValue(self):
        writer = BaseWriter.BaseWriter(None)
        self.assertEqual("Upcoming developments", writer.convertVersion(str(sys.maxsize)))

if __name__ == '__main__':
    unittest.main()