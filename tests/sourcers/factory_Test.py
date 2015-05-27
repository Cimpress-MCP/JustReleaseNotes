import unittest
import JustReleaseNotes.sourcers
from JustReleaseNotes.sourcers import factory

class factory_Test(unittest.TestCase):

    def test_factoryRetrievesGitRepo(self):
        self.assertIsNotNone(JustReleaseNotes.sourcers.factory.create(
            {
               "Provider" : "GitRepo",
               "Directory" : "output",
               "RepositoryUrl" : "https://some.url"
            }))

    def test_failsIfSourcersUnknown(self):
        with self.assertRaises(Exception):
            JustReleaseNotes.sourcers.factory.create({ "Provider": "abrakadabra" })