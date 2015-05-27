import unittest
import JustReleaseNotes.artifacters.versioners
from JustReleaseNotes.artifacters.versioners import factory

class factory_Test(unittest.TestCase):

    def test_factoryRetrievesDll(self):
        self.assertIsNotNone(JustReleaseNotes.artifacters.versioners.factory.create("dll"))

    def test_factoryRetrievesIvy(self):
        self.assertIsNotNone(JustReleaseNotes.artifacters.versioners.factory.create("ivy"))

    def test_failsIfVersionerUnknown(self):
        with self.assertRaises(Exception):
            JustReleaseNotes.artifacters.versioners.factory.create("abrakadabra")