import unittest
import json
from JustReleaseNotes.writers import JsonWriter
from mock import Mock


class JsonWriter_Test(unittest.TestCase):

    def __compareTickets(self, expectedTicket, actualTicket):
        # compares content of an actual ticket
        self.assertEqual(expectedTicket["ticket"], actualTicket["ticket"])
        self.assertEqual(expectedTicket["html_url"], actualTicket["html_url"])
        self.assertEqual(expectedTicket["reporter"], actualTicket["reporter"])
        self.assertEqual(expectedTicket["title"], actualTicket["title"])

    def __compareVersions(self, expectedVersion, actualVersion):
        # compare version
        self.assertEqual(expectedVersion["version"], actualVersion["version"])

        # compare ticket cound
        self.assertEqual(len(expectedVersion["tickets"]), len(actualVersion["tickets"]))
        for i in [1, 2]:
            expectedTicket = next(obj for obj in expectedVersion["tickets"] if obj["ticket"] == "ABCD-{}".format(i))
            actualTicket = next(obj for obj in actualVersion["tickets"] if obj["ticket"] == "ABCD-{}".format(i))
            self.__compareTickets(expectedTicket, actualTicket)

    def test_returnsHtmlExtension(self):
        writer = JsonWriter.JsonWriter(None)
        self.assertEqual(".json", writer.getExtension())

    def ticket_side_effect(*args, **kwargs):
        if args[1] == "ABCD-1":
            return {"title": "ABCD1 ticket", "ticket": "ABCD-1", "html_url": "http://some.url", "reporter" : "test user"}
        elif args[1] == "ABCD-2":
            return {"title": "ABCD2 ticket", "ticket": "ABCD-2", "html_url": "http://some.url", "reporter" : "test user"}
        return None

    def ticket_side_effect_with_embedded_link(*args, **kwargs):
        if args[1] == "ABCD-1":
            return dict(title="ABCD1 ticket that references ABCD-2", ticket="ABCD-1", html_url="http://some.url",
                        embedded_link={"ABCD-2": "http://some.url/ABCD-2"}, reporter="test user")
        elif args[1] == "ABCD-2":
            return dict(title="ABCD2 ticket that references ABCD-1", ticket="ABCD-2", html_url="http://some.url",
                        embedded_link={"ABCD-1": "http://some.url/ABCD-1"}, reporter="test user")
        return None

    def test_givenFairlyCompleteTicketJsonBlockIsGenerated(self):
        self.maxDiff = None
        mockedTicketProvider = Mock()
        mockedTicketProvider.getTicketInfo.side_effect = self.ticket_side_effect

        writer = JsonWriter.JsonWriter(mockedTicketProvider)
        deps = {"ANY": "SomeComponent1: 2.3.*; SomeComponent2: 1.0.0"}
        version = "1.0.2.0"
        date = "01-02-2015"
        tickets = ["ABCD-1", "ABCD-2"]
        output = writer.printVersionBlock(deps, version, date, tickets)

        expected = {"version": "1.0.2.0", "tickets": [
            {"reporter": "test user", "ticket": "ABCD-1", "html_url": "http://some.url", "title": "ABCD1 ticket"},
            {"reporter": "test user", "ticket": "ABCD-2", "html_url": "http://some.url", "title": "ABCD2 ticket"}]}
        actual = json.loads(output)

        # check the length of the ticket, and then loop through the list of tickets and validate the content is the same
        self.__compareVersions(expected, actual)

    def test_setInitialContentParsesJson(self):
        mockedTicketProvider = Mock()
        mockedData= '[ {"version": "1.0.2.0", "tickets": [{"html_url": "http://some.url", "title": "ABCD2 ticket", "reporter": "test user", "ticket": "ABCD-2"}, {"html_url": "http://some.url", "title": "ABCD1 ticket", "reporter": "test user", "ticket": "ABCD-1"}]} ]'
        writer = JsonWriter.JsonWriter(mockedTicketProvider)
        output = writer.setInitialContent(mockedData)
        self.assertEqual(1, len(output))
        expected = json.loads(mockedData)
        self.__compareVersions(expected[0], output["1.0.2.0"])

    def test_printVersionBlockReturnsWhateverIsPresentInitially(self):
        mockedTicketProvider = Mock()
        mockedData = '[ {"version": "1.1.1.1", "tickets": [{"html_url": "http://some.url", "title": "ABCD2 ticket", "reporter": "test user", "ticket": "ABCD-2"}, {"html_url": "http://some.url", "title": "ABCD1 ticket", "reporter": "test user", "ticket": "ABCD-1"}]} ]'
        writer = JsonWriter.JsonWriter(mockedTicketProvider)
        output = writer.setInitialContent(mockedData)
        self.assertEqual(1, len(output))
        expected = json.loads(mockedData)
        actualStr = writer.printVersionBlock(None, "1.1.1.1", None, None)
        actual = json.loads(actualStr)
        self.__compareVersions(expected[0], actual)

    def test_writeDocumentCreatesJsonArray(self):
        writer = JsonWriter.JsonWriter(None)
        result = writer.writeDocument([])
        self.assertEqual("[]", result)

if __name__ == '__main__':
    unittest.main()