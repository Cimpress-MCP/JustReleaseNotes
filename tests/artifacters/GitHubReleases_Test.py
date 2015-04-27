import unittest
from JustReleaseNotes.artifacters import GitHubReleases
import requests
import requests_mock
import sys
import StringIO

class GitHubReleases_Test(unittest.TestCase):

  def setUp(self):
     self.__stdoutSaved = sys.stdout
     self.__out = StringIO.StringIO()
     sys.stdout = self.__out

  def tearDown(self):
     sys.stdout = self.__stdoutSaved

  def test_retrievePromotedVersionsContainsValidVersions(self):
    requests.packages.urllib3.disable_warnings()
    fileContents = '[{"name": "2.0.1.153", "published_at": "2015-04-24T15:24:29Z"},' \
                   '{"name": "1.0.0.15", "published_at": "2015-03-19T23:19:08Z"}]'

    config = { "Authorization" : "token 5dbf862c5197414138e70c4f3fb458c5f5a58f05",
               "Provider" : "GitHubReleases",
               "Url" : "https://api.github.com/repos/cimpress-mcp/PostalCodes.Net/releases"  }

    artifacter = GitHubReleases.GitHubReleases(config);
    with requests_mock.mock() as m:
        m.get('https://api.github.com/repos/cimpress-mcp/PostalCodes.Net/releases', text=fileContents)
        promotedVersion = artifacter.retrievePromotedVersions()
        self.assertIn("1.0.0.15", promotedVersion)
        self.assertIn("2.0.1.153", promotedVersion)
        self.assertTrue(2, len(promotedVersion))
    output = self.__out.getvalue().strip()
    self.assertEquals('GitHub Releases: Retrieving promoted from GitHubReleases at https://api.github.com/repos/cimpress-mcp/PostalCodes.Net/releases ...\n'
                      'GitHub Releases: Found 2 promoted versions',
                      output)

  def test_retrievePromotedVersionsFromEmptyArrayRaises(self):
    requests.packages.urllib3.disable_warnings()
    fileContents = '[]'

    config = { "Authorization" : "token 5dbf862c5197414138e70c4f3fb458c5f5a58f05",
               "Provider" : "GitHubReleases",
               "Url" : "https://api.github.com/repos/cimpress-mcp/PostalCodes.Net/releases"  }

    artifacter = GitHubReleases.GitHubReleases(config);
    with requests_mock.mock() as m:
        m.get('https://api.github.com/repos/cimpress-mcp/PostalCodes.Net/releases', text=fileContents)
        with self.assertRaises(ValueError):
            artifacter.retrievePromotedVersions()

if __name__ == '__main__':
    unittest.main()