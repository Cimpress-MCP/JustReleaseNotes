import unittest
from JustReleaseNotes.writers import MarkdownWriter
from mock import MagicMock
from mock import Mock


class MarkdownWriter_Test(unittest.TestCase):
    def test_returnsMdExtension(self):
        writer = MarkdownWriter.MarkdownWriter(None)
        self.assertEqual(".md", writer.getExtension())

    def ticket_side_effect(*args, **kwargs):
        if args[1] == "DBA-1":
            return {"title": "DBA1 ticket", "ticket": "DBA-1", "html_url": "http://some.url"}
        elif args[1] == "DBA-2":
            return {"title": "DBA2 ticket", "ticket": "DBA-2", "html_url": "http://some.url"}
        return None

    def ticket_side_effect_with_embedded_link(*args, **kwargs):
        if args[1] == "DBA-1":
            return dict(title="DBA1 ticket that references #DBA-2", ticket="DBA-1", html_url="http://some.url",
                        embedded_link={"#DBA-2": "http://some.url/DBA-2"})
        elif args[1] == "DBA-2":
            return dict(title="DBA2 ticket that references #DBA-1", ticket="DBA-2", html_url="http://some.url",
                        embedded_link={"#DBA-1": "http://some.url/DBA-1"})
        return None


    def test_givenFairlyCompleteTicketMarkdownBlockIsGenerated(self):
        mockedTicketProvider = Mock()
        mockedTicketProvider.getTicketInfo = self.ticket_side_effect

        writer = MarkdownWriter.MarkdownWriter(mockedTicketProvider)
        deps = {"ANY": "SomeComponent1: 2.3.*; SomeComponent2: 1.0.0"}
        version = "1.0.2.0"
        date = "01-02-2015"
        tickets = ["DBA-1", "DBA-2"]
        output = writer.printVersionBlock(deps, version, date, tickets)
        self.assertEqual(
            '## 1.0.2.0 ##\n01-02-2015\n\n*  [DBA-2](http://some.url) DBA2 ticket\n*  [DBA-1](http://some.url) DBA1 ticket\n',
            output)


    def test_embeddedLinkProvided_ReplacesContentWithLink(self):
        mockedTicketProvider = Mock()
        mockedTicketProvider.getTicketInfo = self.ticket_side_effect_with_embedded_link

        writer = MarkdownWriter.MarkdownWriter(mockedTicketProvider)
        deps = {"ANY": "SomeComponent1: 2.3.*; SomeComponent2: 1.0.0"}
        version = "1.0.2.0"
        date = "01-02-2015"
        tickets = ["DBA-1", "DBA-2"]
        output = writer.printVersionBlock(deps, version, date, tickets)
        self.assertEqual(
            '## 1.0.2.0 ##\n01-02-2015\n\n*  [DBA-2](http://some.url) DBA2 ticket that references [#DBA-1](http://some.url/DBA-1)\n*  '
            '[DBA-1](http://some.url) DBA1 ticket that references [#DBA-2](http://some.url/DBA-2)\n',
            output)


if __name__ == '__main__':
    unittest.main()