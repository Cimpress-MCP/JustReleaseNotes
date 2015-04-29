import unittest
import os
from JustReleaseNotes.utils import EnvReplacer
from mock import MagicMock
from mock import Mock

class EnvParser_Test(unittest.TestCase):

    def test_listWithNoEnvStaysTheSame(self):
        conf = [1,2,3]
        self.assertEqual(conf, EnvReplacer.replace(conf))

    def test_primitiveWithNoEnvStaysTheSame(self):
        conf = 1
        self.assertEqual(conf, EnvReplacer.replace(conf))

    def test_dictWithNoEnvStaysTheSame(self):
        conf = {
            "a" : "bb",
            "b" : [1, 2, 3, 4.5, "1231"],
            "c" : {
                "x" : "y"
            }
        }
        self.assertEqual(conf, EnvReplacer.replace(conf))

    def test_dictWithEnvParsedCorrectly(self):
        os.environ['abc'] = 'xyz'
        os.environ['ab_12'] = "xy99"
        os.environ['AbAb'] = "ZZZ"
        conf = {
            "a" : "bb",
            "b" : [1, 2, 3, 4.5, "ENV[abc]"],
            "c" : {
                "x" : "env[ab_12]",
                "d" : "Env[AbAb] x eNV[AbAb]"
            }
        }
        expectedConf = {
            "a" : "bb",
            "b" : [1, 2, 3, 4.5, "xyz"],
            "c" : {
                "x" : "xy99",
                "d" : "ZZZ x ZZZ"
            }
        }
        self.assertEqual(expectedConf, EnvReplacer.replace(conf))

if __name__ == '__main__':
    unittest.main()