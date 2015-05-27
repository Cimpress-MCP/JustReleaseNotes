import unittest
import JustReleaseNotes.artifacters
from JustReleaseNotes.artifacters import factory

class factory_Test(unittest.TestCase):

    def test_factoryRetrievesArtifactory(self):
        self.assertIsNotNone(JustReleaseNotes.artifacters.factory.create(
            {
              "Provider" : "Artifactory",
              "Repository" : "libs-release-local",
              "ArtifactUri" : "/com.vistaprint/QP.Quoter",
              "StorageUrl" : "http://artifactory.vistaprint.net/api/storage",
              "DirectDependencies" : {
                "ANY" : {
                    "type" : "ivy"
                }
            }}))

    def test_factoryRetrievesGitHubReleases(self):
        self.assertIsNotNone(JustReleaseNotes.artifacters.factory.create(
            {
              "Provider" : "GitHubReleases",
              "HtmlUrl" : "https://some.url",
              "Authorization" : "token 0dad61692abe6ae1ecb9b4a3a10483a4b8bd61fd",
              "Url" : "https://api.some.url"
            }))

    def test_failsIfArtifacterUnknown(self):
        with self.assertRaises(Exception):
            JustReleaseNotes.artifacters.factory.create({ "Provider": "abrakadabra" })