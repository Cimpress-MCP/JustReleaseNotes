import unittest
import JustReleaseNotes.artifacters.versioners
from JustReleaseNotes.artifacters.versioners import factory


class GitHubReleases_Test(unittest.TestCase):

  def test_retrievePromotedVersionsContainsValidVersions(self):

    fileContents = bytes('<ivy-module version="1.0"><info organisation="org.apache" module="dependee"/>' \
                   '<dependencies>' \
                   '</dependencies>' \
                   '</ivy-module>')

    versioner = JustReleaseNotes.artifacters.versioners.factory.create("ivy");
    versions = versioner.extractVersions(fileContents, "Ivy.xml")
    self.assertEqual(0, len(versions))

  def test_retrievePromotedVersionsContainsValidVersions(self):

    fileContents = bytes('<ivy-module version="1.0"><info organisation="org.apache" module="dependee"/>' \
                   '<dependencies>' \
                   '<dependency org="commons-lang" name="commons-lang" rev="2.0"/>' \
                   '</dependencies>' \
                   '</ivy-module>')

    versioner = JustReleaseNotes.artifacters.versioners.factory.create("ivy");
    versions = versioner.extractVersions(fileContents, "Ivy.xml")
    self.assertIn("commons-lang: 2.0", versions)
    self.assertEqual(1, len(versions))


  def test_retrievePromotedVersionsContainsValidVersions(self):

    fileContents = bytes('<ivy-module version="1.0"><info organisation="org.apache" module="dependee"/>' \
                   '<dependencies>' \
                   '<dependency org="commons-lang" name="commons-lang" rev="2.0"/>' \
                   '<dependency org="commons-lang" name="weirdVersionComponent" rev="121.23.0.*"/>' \
                   '</dependencies>' \
                   '</ivy-module>')

    versioner = JustReleaseNotes.artifacters.versioners.factory.create("ivy");
    versions = versioner.extractVersions(fileContents, "Ivy.xml")
    self.assertIn("commons-lang: 2.0", versions)
    self.assertIn("weirdVersionComponent: 121.23.0.*", versions)
    self.assertEqual(2, len(versions))


if __name__ == '__main__':
    unittest.main()