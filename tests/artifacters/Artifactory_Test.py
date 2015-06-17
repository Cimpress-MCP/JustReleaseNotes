import unittest
from JustReleaseNotes.artifacters import Artifactory
import requests
import requests_mock
import sys
from mock import patch, MagicMock

class Artifactory_Test(unittest.TestCase):

  def setUp(self):
    self.__stdoutSaved = sys.stdout
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO
    self.__out = StringIO()
    sys.stdout = self.__out

  def tearDown(self):
    sys.stdout = self.__stdoutSaved

  def test_retrievePromotedVersionsContainsValidVersions(self):
    requests.packages.urllib3.disable_warnings()
    fileContents = '{ "children": [ { "uri" : "/1.0.0.15" }, { "uri" : "/2.0.1.153" } ]  }'

    config = { "Provider" : "Artifactory",
               "Repository" : "libs-release-local",
               "ArtifactUri" : "org/component",
               "StorageUrl" : "http://artifactory/api/storage" }

    artifacter = Artifactory.Artifactory(config);
    with requests_mock.mock() as m:
        m.get('http://artifactory/api/storage/libs-release-local/org/component', text=fileContents)
        m.get('http://artifactory/api/storage/libs-release-local/org/component/1.0.0.15', text='{ "created" : "2004-10-10" }')
        m.get('http://artifactory/api/storage/libs-release-local/org/component/2.0.1.153', text='{  }')
        promotedVersion = artifacter.retrievePromotedVersions()
        self.assertIn("1.0.0.15", promotedVersion)
        self.assertIn("2.0.1.153", promotedVersion)
        self.assertTrue(2, len(promotedVersion))
    sys.stdout = self.__stdoutSaved
    self.assertEquals('Artifactory: Retrieving promoted (libs-release-local) versions org/component ...\n'
                      'Artifactory: Retrieving info for version 1.0.0.15\n'
                      'Artifactory: Retrieving info for version 2.0.1.153\n'
                      'Artifactory: No \'created\' for version 2.0.1.153\n'
                      'Artifactory: Found 2 promoted versions\n',
                      self.__out.getvalue())

  def test_retrievePromotedVersionsFromEmptyArrayRaises(self):
    requests.packages.urllib3.disable_warnings()
    fileContents = '{ "children" : [] }'

    config = { "Provider" : "Artifactory",
               "Repository" : "libs-release-local",
               "ArtifactUri" : "/org/component",
               "StorageUrl" : "http://artifactory/api/storage" }

    artifacter = Artifactory.Artifactory(config);
    with requests_mock.mock() as m:
        m.get('http://artifactory/api/storage/libs-release-local/org/component', text=fileContents)
        with self.assertRaises(ValueError):
            artifacter.retrievePromotedVersions()

  @patch("JustReleaseNotes.artifacters.versioners.factory.create")
  def test_retrieveDependeciesVersions(self, mocked_versioner):
    requests.packages.urllib3.disable_warnings()

    config = { "Provider" : "Artifactory",
               "Repository" : "libs-release-local",
               "ArtifactUri" : "org/component",
               "StorageUrl" : "http://artifactory/api/storage",
               "DirectDependencies" : {
                    "SomePackage" : {
                        "type" : "dll",
                        "name" : "some_package"
                    }
               }
             }

    versioner = MagicMock();
    versioner.extractVersions.return_value = ['9.9']
    mocked_versioner.return_value = versioner

    artifacter = Artifactory.Artifactory(config);
    with requests_mock.mock() as m:
        m.get('http://artifactory/api/storage/libs-release-local/org/component/0.1.2/some_package', text='{ "downloadUri" : "http://some.url/9.9/file" }' )
        m.get('http://some.url/9.9/file', text='ContentOfFileWithVersion9.9')
        result = artifacter.retrieveDependeciesVersions("0.1.2")
    self.assertEqual("9.9", result["SomePackage"]);


if __name__ == '__main__':
    unittest.main()