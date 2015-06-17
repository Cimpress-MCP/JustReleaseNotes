import unittest
import mock
from mock import patch
from JustReleaseNotes.issuers import GitHubIssues
import requests
import requests_mock
import JustReleaseNotes.issuers.AggregateIssuer

class DummyIssuer:

    __ret = None

    def __init__(self, value):
        self.__ret = value

    def extractTicketsFromMessage(self, message):
        return [self.__ret] if self.__ret in message else ["NULL"]

    def getTicketInfo(self, ticket):
        if self.__ret == ticket:
            return { "ticket" : self.__ret, "title" : "Title of " + self.__ret }
        else:
            raise

class GitHubIssues_Test(unittest.TestCase):

  @patch('JustReleaseNotes.issuers.factory.create')
  def test_extractTicketsFromMessage_ReturnsTicketsExtractedByEachOfIssuers(self, mock_class):
      mock_class.side_effect = [DummyIssuer("first-1"), DummyIssuer("second-1")]

      config = [{ "Provider" : "first"},{ "Provider":"second"}]
      issuer = JustReleaseNotes.issuers.AggregateIssuer.AggregateIssuer(config)
      ret = issuer.extractTicketsFromMessage("Message containing first-1 and second-1")
      self.assertIn("first-1", ret)
      self.assertIn("second-1", ret)

  @patch('JustReleaseNotes.issuers.factory.create')
  def test_getTicketInfo_ReturnsTicketsExtractedByEachOfIssuers(self, mock_class):
      mock_class.side_effect = [DummyIssuer("first-1"), DummyIssuer("second-1")]

      config = [{ "Provider" : "first"},{ "Provider":"second"}]
      issuer = JustReleaseNotes.issuers.AggregateIssuer.AggregateIssuer(config)
      ret = issuer.getTicketInfo("first-1")
      self.assertIn("first-1", ret["ticket"])
      self.assertIn("Title of first-1", ret["title"])
      ret = issuer.getTicketInfo("second-1")
      self.assertIn("second-1", ret["ticket"])
      self.assertIn("Title of second-1", ret["title"])

  @patch('JustReleaseNotes.issuers.factory.create')
  def test_noIssuersReturnsNone(self, mock_class):
      mock_class.side_effect = []
      config = []
      issuer = JustReleaseNotes.issuers.AggregateIssuer.AggregateIssuer(config)
      ret = issuer.getTicketInfo("first-1")
      self.assertEqual(None, ret)


if __name__ == '__main__':
    unittest.main()