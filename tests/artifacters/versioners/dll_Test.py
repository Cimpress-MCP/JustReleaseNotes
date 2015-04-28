import unittest
import JustReleaseNotes.artifacters.versioners
from JustReleaseNotes.artifacters.versioners import factory
import os
import inspect

class GitHubReleases_Test(unittest.TestCase):

  def test_retrievePromotedVersionsContainsValidVersions(self):

    dllFile = os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), "test.dll")
    f = open(dllFile, "rb");
    fileContents = bytes(f.read())
    versioner = JustReleaseNotes.artifacters.versioners.factory.create("dll");
    versions = versioner.extractVersions(fileContents, "test.dll")
    self.assertEqual(1, len(versions))
    self.assertIn("test.dll: 2.1.0.0", versions);

if __name__ == '__main__':
    unittest.main()