import unittest
from JustReleaseNotes.artifacters import GitHubReleases
from mocker import Mocker
import requests
import os

class GitHubReleases_Test(unittest.TestCase):

  def test_retrievePromotedVersions(self):
    requests.packages.urllib3.disable_warnings()
    fileContents = '[{"name": "2.0.1.153", "published_at": "2015-04-24T15:24:29Z"},' \
                   '{"name": "1.0.0.15", "published_at": "2015-03-19T23:19:08Z"}]'

    config = { "Authorization" : "token 5dbf862c5197414138e70c4f3fb458c5f5a58f05",
               "Provider" : "GitHubReleases",
               "Url" : "https://api.github.com/repos/cimpress-mcp/PostalCodes.Net/releases"  }

    artifacter = GitHubReleases.GitHubReleases(config);

    mocker = Mocker()

    result = mocker.mock()
    result.text
    mocker.result(fileContents)

    myget = mocker.replace("requests.get")
    myget('https://api.github.com/repos/cimpress-mcp/PostalCodes.Net/releases',
         headers = { "Authorization": "token 5dbf862c5197414138e70c4f3fb458c5f5a58f05"}, verify=False)
    mocker.result(result)

    mocker.replay()
    promotedVersion = artifacter.retrievePromotedVersions()
    self.assertIn("1.0.0.15", promotedVersion)
    self.assertIn("2.0.1.153", promotedVersion)
    self.assertTrue(2, len(promotedVersion))
    mocker.verify()

if __name__ == '__main__':
    unittest.main()