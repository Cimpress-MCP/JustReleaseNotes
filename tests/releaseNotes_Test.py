import unittest
from datetime import datetime
import JustReleaseNotes
from mock import Mock, MagicMock
from JustReleaseNotes import releaseNotes

class ReleaseNote_Test(unittest.TestCase):

    def test_givenSimpleInputPrintVersionBlockGetsCalled(self):

        conf = {}
        conf["Source"] = {}
        conf["Source"]["OldestCommitToProcess"] = "ef334212ab2323a32323"
        promotedVersions = {}
        ticketProvider = Mock()
        ticketProvider.extractTicketsFromMessage = MagicMock(return_value=["TCKT-1"])
        ticketProvider.getTicketInfo = MagicMock(return_value={ "issue_type_icon" : "None", "html_url" : None,
                                                                "ticket" : "TCKT-1",   "title" : "TCKT-1 Summary",
                                                                "embedded_link" : {} })
        writer = Mock()
        writer.printVersionBlock = MagicMock(return_value="empty")
        repo = Mock()
        repo.gitCommitsList = ["ef334212ab2323a32323",
                               "as5d4a5sd4a5sd4a5sd4"]
        repo.versionsByGitHash = {"ef334212ab2323a32323": "1.0.1.2",
                                  "as5d4a5sd4a5sd4a5sd4": "1.0.1.1"}
        repo.gitHistoryByVersion = {"1.0.1.2": ["ef334212ab2323a32323"],
                                    "1.0.1.1": ["as5d4a5sd4a5sd4a5sd4"]}
        repo.gitCommitMessagesByHash = {"ef334212ab2323a32323": "Something about TCKT-1",
                                        "as5d4a5sd4a5sd4a5sd4": "Something about TCKT-0"}
        repo.gitDatesByHash = {"ef334212ab2323a32323" : datetime.strptime("2015-12-12 12:12:12", "%Y-%m-%d %H:%M:%S").toordinal(),
                               "as5d4a5sd4a5sd4a5sd4" : datetime.strptime("2015-11-11 11:11:11", "%Y-%m-%d %H:%M:%S").toordinal()}

        releaseNotes = JustReleaseNotes.releaseNotes.ReleaseNotes(conf, ticketProvider, repo, promotedVersions)
        releaseNotes.generateReleaseNotesByPromotedVersions(writer)
        writer.printVersionBlock.assert_called_once_with({}, "1.0.1.2", "N/A", ["TCKT-1"])

if __name__ == '__main__':
    unittest.main()
