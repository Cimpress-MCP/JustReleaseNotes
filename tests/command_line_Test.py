import unittest
import JustReleaseNotes.command_line
import sys, os
from mock import Mock, MagicMock, mock_open, patch

from sys import version_info

if version_info.major == 2:
    import __builtin__ as builtins
else:
    import builtins


class ReleaseNote_Test(unittest.TestCase):

    @patch("JustReleaseNotes.issuers.factory")
    @patch("JustReleaseNotes.sourcers.factory")
    @patch("JustReleaseNotes.writers.factory")
    @patch("os.path.exists")
    @patch("os.makedirs")
    def test_justRelesdeNotes_withDefaultConfig_NoData_DoesNotRaise_ProducesEmptyOutput(self, issuers_factory, repo_factory,
        writers_factory, path_exists, path_makedirs):

        writer_mock = MagicMock()
        writers_factory.create.return_value = writer_mock
        writer_mock.getExtension.return_value = ".ext"

        mocked_open = mock_open(
                read_data='{ '
                          '"pathToSave": "..", '
                          '"packages": { '
                          '     "JustReleaseNotes": { '
                          '     "Issues": { '
                          '         "Provider": "TestProvider",     '
                          '         "HtmlUrl": "https://Just.Release.Notes/issues", '
                          '         "Url": "https://Just.Release.Notes/issues" }, '
                          '     "Source": { '
                          '         "Provider": "TestRepo", '
                          '         "RepositoryUrl": '
                          '         "https://Just.Release.Notes/repo.git" '
                          '     }, '
                          '     "ReleaseNotesWriter": "TestWriter" '
                          '   }'
                          ' } '
                          '}')

        with patch.object(builtins, 'open', mocked_open):
            JustReleaseNotes.command_line.main()

        mocked_open.assert_called_with(os.getcwd() + "/../JustReleaseNotes/index.ext", "wb")
        mocked_open().write.assert_called_once_with(b'')


if __name__ == '__main__':
    unittest.main()
