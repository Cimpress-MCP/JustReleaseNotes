import unittest
from JustReleaseNotes.writers import MarkdownWriter
from mock import Mock, MagicMock, mock_open, patch
from mock import Mock
from sys import version_info

if version_info.major == 2:
    import __builtin__ as builtins
else:
    import builtins

class MarkdownWriter_Test(unittest.TestCase):
    def test_returnsMdExtension(self):
        writer = MarkdownWriter.MarkdownWriter(None)
        self.assertEqual(".md", writer.getExtension())

    def ticket_side_effect(*args, **kwargs):
        if args[1] == "DBA-1":
            return {"title": "DBA1 ticket", "ticket": "DBA-1", "html_url": "http://some.url", "reporter" : "test user"}
        elif args[1] == "DBA-2":
            return {"title": "DBA2 ticket", "ticket": "DBA-2", "html_url": "http://some.url", "reporter" : "test user"}
        return None

    def ticket_side_effect_with_embedded_link(*args, **kwargs):
        if args[1] == "DBA-1":
            return dict(title="DBA1 ticket that references #DBA-2", ticket="DBA-1", html_url="http://some.url",
                        embedded_link={"#DBA-2": "http://some.url/DBA-2"}, reporter="test user")
        elif args[1] == "DBA-2":
            return dict(title="DBA2 ticket that references #DBA-1", ticket="DBA-2", html_url="http://some.url",
                        embedded_link={"#DBA-1": "http://some.url/DBA-1"}, reporter="test user")
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
            '## 1.0.2.0 ##\n01-02-2015\n\n*  [DBA-2](http://some.url) DBA2 ticket\n*'
            '  [DBA-1](http://some.url) DBA1 ticket, reported by test user\n',
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
            '## 1.0.2.0 ##\n01-02-2015\n\n* [DBA-2](http://some.url) DBA2 ticket that references'
            ' [#DBA-1](http://some.url/DBA-1), *reported by* **test user**\n* [DBA-1](http://some.url) DBA1 ticket that references '
            '[#DBA-2](http://some.url/DBA-2), *reported by* **test user**\n',
            output)

    def test_versionHeaderParsingAndGenerationAreCompatible(self):
        mockedTicketProvider = Mock()
        writer = MarkdownWriter.MarkdownWriter(mockedTicketProvider)
        self.assertEqual("1.2.3", writer.parseVersionHeader(writer.getVersionHeader("1.2.3")))

    def test_givenFairlyCompleteTicketMarkdownBlockIsGenerated(self):
        mockedTicketProvider = Mock()
        writer = MarkdownWriter.MarkdownWriter(mockedTicketProvider)
        self.assertEqual("![Icon](http://icon.url/image.png)",
                         writer.getImageBlock("http://icon.url/image.png"));

    def test_setInitialContentParsesMarkdown(self):
        mockedTicketProvider = Mock()
        mockedData='## Upcoming developments ##\n03-02-2015\n\n' \
                   '*  [DBA-3](http://some.url) DBA2 ticket that references \n' \
                   '*  [DBA-4](http://some.url) DBA1 ticket that references \n' \
                   '## 1.0.2.0 ##\n02-02-2015\n\n' \
                   '*  [DBA-2](http://some.url) DBA2 ticket that references [#DBA-1](http://some.url/DBA-1), reported by test user\n' \
                   '*  [DBA-1](http://some.url) DBA1 ticket that references [#DBA-2](http://some.url/DBA-2), reported by test user\n' \
                   '## 1.0.0.1 ##\n01-02-2015\n\n' \
                   '*  [DBA-3](http://some.url) DBA2 ticket that references \n' \
                   '*  [DBA-4](http://some.url) DBA1 ticket that references \n'
        writer = MarkdownWriter.MarkdownWriter(mockedTicketProvider)
        output = writer.setInitialContent(mockedData)
        self.assertEqual(2, len(output))
        self.assertEqual(["## 1.0.2.0 ##",
                           "02-02-2015",
                           '',
                           "*  [DBA-2](http://some.url) DBA2 ticket that references [#DBA-1](http://some.url/DBA-1), reported by test user",
                           "*  [DBA-1](http://some.url) DBA1 ticket that references [#DBA-2](http://some.url/DBA-2), reported by test user"
                           ], output["1.0.2.0"])
        self.assertEqual(['## 1.0.0.1 ##',
                           '01-02-2015',
                           '',
                           '*  [DBA-3](http://some.url) DBA2 ticket that references ',
                           '*  [DBA-4](http://some.url) DBA1 ticket that references ',
                           ''
                           ], output["1.0.0.1"])

    def test_printVersionBlockReturnsWhateverIsPresentInitially(self):
        mockedTicketProvider = Mock()
        mockedData='## 1.0.0.1 ##\n' \
                   'SomeCustomStuff' \
                   'possibly even unstructured\n some comments etc\n'
        writer = MarkdownWriter.MarkdownWriter(mockedTicketProvider)
        output = writer.setInitialContent(mockedData)
        self.assertEqual(1, len(output))
        self.assertEqual(mockedData, writer.printVersionBlock(None, "1.0.0.1", None, None))

    def test_printVersionBlockHandlesIntDate(self):
        mockedTicketProvider = Mock()
        mockedTicketProvider.getTicketInfo = self.ticket_side_effect

        writer = MarkdownWriter.MarkdownWriter(mockedTicketProvider)
        deps = {"ANY": "SomeComponent1: 2.3.*; SomeComponent2: 1.0.0"}
        version = "1.0.2.0"
        date = 1422798811
        tickets = ["DBA-1", "DBA-2"]
        output = writer.printVersionBlock(deps, version, date, tickets)
        self.assertEqual(
            "## 1.0.2.0 ##\n2015-02-01\n\n* [DBA-2](http://some.url) DBA2 ticket, *reported by* **test user**\n* [DBA-1](http://some.url) DBA1 ticket, *reported by* **test user**\n",
            output)


if __name__ == '__main__':
    unittest.main()