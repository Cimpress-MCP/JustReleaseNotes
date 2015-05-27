import unittest
import JustReleaseNotes
from mock import Mock, MagicMock
from JustReleaseNotes import releaseNotes

class ReleaseNote_Test(unittest.TestCase):

    def test_givenSimpleInputPrintVersionBlockGetsCalled(self):

        conf = {}
        promotedVersions = {}
        ticketProvider = Mock()
        ticketProvider.extractTicketsFromMessage = MagicMock(return_value=["TCKT-1"])
        ticketProvider.getTicketInfo = MagicMock(return_value={ "issue_type_icon" : "None", "html_url" : None,
                                                                "ticket" : "TCKT-1",   "title" : "TCKT-1 Summary",
                                                                "embedded_link" : {} })
        writer = Mock()
        writer.printVersionBlock = MagicMock(return_value="empty")
        repo = Mock()
        repo.gitCommitsList = ["ef334212ab2323a32323"]
        repo.versionsByGitHash = { "ef334212ab2323a32323" : "1.0.1.2"}
        repo.gitHistoryByVersion = {"1.0.1.2" : ["ef334212ab2323a32323"]}
        repo.gitCommitMessagesByHash = { "ef334212ab2323a32323" : "Something about TCKT-1"}


        releaseNotes = JustReleaseNotes.releaseNotes.ReleaseNotes(conf, ticketProvider, writer, repo, promotedVersions)
        releaseNotes.generateReleaseNotesByPromotedVersions()
        writer.printVersionBlock.assert_called_once_with({}, "1.0.1.2", "N/A", ["TCKT-1"])

if __name__ == '__main__':
    unittest.main()
