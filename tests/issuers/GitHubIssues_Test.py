import unittest
from JustReleaseNotes.issuers import GitHubIssues
import requests
import requests_mock

class GitHubIssues_Test(unittest.TestCase):

  def test_retrieveIssueInfoWhenNoCachedData_ConnectsToTheSource(self):
    requests.packages.urllib3.disable_warnings()
    ticketResponse = '{ "html_url" : "https://api.github.com/repos/cimpress-mcp/PostalCodes.Net/issues/23", ' \
                     '"title" : "Ticket\'s title" }'

    config = { "Provider" : "GitHubIssues",
               "HtmlUrl" : "https://github.com/Cimpress-mcp/PostalCodes.Net/issues",
               "Authorization" : "token someToken",
               "Url" : "https://api.github.com/repos/cimpress-mcp/PostalCodes.Net/issues" }

    with requests_mock.mock() as m:
        m.get('https://api.github.com/repos/cimpress-mcp/PostalCodes.Net/issues/23', text=ticketResponse)
        m.get('https://api.github.com/repos/cimpress-mcp/PostalCodes.Net/issues?filter=all&state=all', text='{}')
        issuer = GitHubIssues.GitHubIssues(config);

        ticketInfo = issuer.getTicketInfo("23")
        self.assertEqual("#23", ticketInfo["ticket"])
        self.assertEqual("Ticket's title", ticketInfo["title"])

if __name__ == '__main__':
    unittest.main()