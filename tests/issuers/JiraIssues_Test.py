import unittest
from JustReleaseNotes.issuers import JiraIssues
import requests
import requests_mock

class JiraIssues_Test(unittest.TestCase):

  def test_retrieveIssueInfoWhenNoCachedData_ConnectsToTheSource(self):
    requests.packages.urllib3.disable_warnings()
    ticketResponse = bytearray('{ "html_url" : "https://api.github.com/repos/cimpress-mcp/PostalCodes.Net/issues/23", ' \
                     '"title" : "Ticket\'s title",' \
                     '"fields" : {' \
                     '"summary" : "Title of TCKT-23",' \
                     '"status" : { "name" : "New", "iconUrl" : "http://site.com/imageUrl.png" },' \
                     '"issuetype" : { "name" : "Task", "iconUrl" : "http://site.com/imageUrl.png" },'\
                     '"priority" : { "name" : "Critical", "iconUrl" : "http://site.com/imageUrl.png" },'\
                     '"labels" : [],'\
                     '"reporter" : { "displayName" : "', 'utf-8')

    # add an unicode character
    ticketResponse.append(0xc4)
    ticketResponse.append(0xb1)
    for x in bytearray('" } } }', 'utf-8'):
        ticketResponse.append(x)

    config = { "Provider" : "JiraIssues",
               "HtmlUrl" : "https://jira.com/issues",
               "Authorization" : "token someToken",
               "Url" : "https://jira.com/rest/api/2/issues" }

    with requests_mock.mock() as m:
        m.get('https://jira.com/rest/api/2/issues/TCKT-23', text=ticketResponse.decode('utf-8'))
        issuer = JiraIssues.JiraIssues(config);

        ticketInfo = issuer.getTicketInfo("TCKT-23")
        self.assertEqual("TCKT-23", ticketInfo["ticket"])
        self.assertEqual("Title of TCKT-23", ticketInfo["title"])

if __name__ == '__main__':
    unittest.main()