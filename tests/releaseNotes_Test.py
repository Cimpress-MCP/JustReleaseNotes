# -*- coding: utf-8 -*-

import unittest
from datetime import datetime
import JustReleaseNotes
from mock import Mock, MagicMock
from JustReleaseNotes import releaseNotes
from JustReleaseNotes.writers import MarkdownWriter


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
                                                                "embedded_link" : {}, "reporter" : "rnowosielski" })
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
        writer.printVersionBlock.assert_called_once_with({}, "1.0.1.2", 735944, ["TCKT-1"])

    def test_givenUnicodeCharacterInTheInitialContent_DoesntFail(self):

        conf = {}
        conf["Source"] = {}
        conf["Source"]["OldestCommitToProcess"] = "ef334212ab2323a32323"
        promotedVersions = {}
        ticketProvider = Mock()
        ticketProvider.extractTicketsFromMessage = MagicMock(return_value=["TCKT-1"])
        ticketProvider.getTicketInfo = MagicMock(return_value={ "issue_type_icon" : "None", "html_url" : None,
                                                                "ticket" : "TCKT-1",   "title" : "TCKT-1 Summary",
                                                                "embedded_link" : {}, "reporter" : "rnowosielski" })
        writer = MarkdownWriter.MarkdownWriter(ticketProvider)
        mockedData='## Upcoming developments ##\n03-02-2015\n\n' \
           '*  [DBA-3](http://some.url) DBA2 ticket that references \n' \
           '*  [DBA-4](http://some.url) DBA1 ticket that references \n' \
           '## 1.0.1.2 ##\n02-02-2015\n\n' \
           '*  [DBA-2](http://some.url) DBA2ı ticket that references [#DBA-1](http://some.url/DBA-1), reported by test user\n' \
           '*  [DBA-1](http://some.url) DBA1 ticket ıthat references [#DBA-2](http://some.url/DBA-2), reported by test user\n' \
           '## 1.0.1.1 ##\n01-02-2015\n\n' \
           '*  [DBA-3](http://some.url) DBA2 ticket that references \n' \
           '*  [DBA-4](http://some.url) DBA1 ticket that references \n'
        writer.setInitialContent(mockedData)

        repo = Mock()
        repo.gitCommitsList = ["ef334212ab2323a32323",
                               "as5d4a5sd4a5sd4a5sd4"]
        repo.versionsByGitHash = {"ef334212ab2323a32323": "1.0.1.2",
                                  "as5d4a5sd4a5sd4a5sd4": "1.0.1.1"}
        repo.gitHistoryByVersion = {"1.0.1.2": ["ef334212ab2323a32323"],
                                    "1.0.1.1": ["as5d4a5sd4a5sd4a5sd4"]}
        repo.gitCommitMessagesByHash = {"ef334212ab2323a32323": "Someting about TCKT-1",
                                        "as5d4a5sd4a5sd4a5sd4": "Something about TCKT-0"}
        repo.gitDatesByHash = {"ef334212ab2323a32323" : datetime.strptime("2015-12-12 12:12:12", "%Y-%m-%d %H:%M:%S").toordinal(),
                               "as5d4a5sd4a5sd4a5sd4" : datetime.strptime("2015-11-11 11:11:11", "%Y-%m-%d %H:%M:%S").toordinal()}

        releaseNotes = JustReleaseNotes.releaseNotes.ReleaseNotes(conf, ticketProvider, repo, promotedVersions)
        output = releaseNotes.generateReleaseNotesByPromotedVersions(writer)



if __name__ == '__main__':
    unittest.main()
