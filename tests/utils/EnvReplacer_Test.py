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

    def test_stringWithNonExistentEnvVariableRaises(self):
        conf = "ENV[non_existing_env_key]"
        self.assertRaises(KeyError, EnvReplacer.replace, conf)

    def test_stringWithEmptyEnvKeyStaysTheSame(self):
        conf = "ENV[]"
        self.assertEqual(conf, EnvReplacer.replace(conf))

    def test_stringWithInvalidEnvKeyStaysTheSame(self):
        conf = "ENV[ ]"
        self.assertEqual(conf, EnvReplacer.replace(conf))

    def test_stringWithMixedCaseEnvIsReplaced(self):
        os.environ["a"] = "1"
        os.environ["b"] = "2"
        os.environ["c"] = "3"
        conf = "env[a] Env[b] ENV[c]"
        self.assertEqual("1 2 3", EnvReplacer.replace(conf))

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

    def test_dictWithUnicodeEnvRaplacedCorrectly(self):
        os.environ['abc'] = 'xyz'
        os.environ['ab_12'] = "xy99"
        os.environ['AbAb'] = "ZZZ"
        conf = {
            u"a" : "ENV[abc]",
            "c" : {
                u"x" : "env[ab_12]",
                u"d" : "Env[AbAb] x eNV[AbAb]"
            }
        }
        expectedConf = {
            u"a" : "xyz",
            "c" : {
                u"x" : "xy99",
                u"d" : "ZZZ x ZZZ"
            }
        }
        self.assertEqual(expectedConf, EnvReplacer.replace(conf))

if __name__ == '__main__':
    unittest.main()
