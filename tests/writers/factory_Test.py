import unittest
from mock import Mock
import JustReleaseNotes.writers
from JustReleaseNotes.writers import factory

class factory_Test(unittest.TestCase):

    def test_factoryRetrievesMarkdownWriter(self):
        ticketProvider = Mock()
        self.assertIsNotNone(JustReleaseNotes.writers.factory.create("MarkdownWriter", ticketProvider))

    def test_factoryRetrievesHtmlWriter(self):
        ticketProvider = Mock()
        self.assertIsNotNone(JustReleaseNotes.writers.factory.create("HtmlWriter", ticketProvider))

    def test_failsIfIssuerUnknown(self):
        with self.assertRaises(Exception):
            JustReleaseNotes.issuers.writers.factory.create("abrakadabra", None)