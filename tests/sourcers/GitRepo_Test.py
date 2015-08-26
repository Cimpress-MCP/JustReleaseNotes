import unittest
from JustReleaseNotes.sourcers import GitRepo
from mock import Mock, MagicMock, mock_open, patch

class GitRepo_Test(unittest.TestCase):

    @patch("git.Repo.clone_from")
    @patch("os.path.isdir")
    @patch("os.makedirs")
    def test_checkourt(self, makedirs_mock, isdir_mock, repo_mock):
        isdir_mock.return_value = False
        conf = { "Directory" : "testDir", "RepositoryUrl" : "git://some.url/repo.git" }
        repo = GitRepo.GitRepo(conf)
        repo.checkout()

        isdir_mock.assert_called_once_with("testDir")
        makedirs_mock.assert_called_once_with("testDir")


    @patch("git.Repo.clone_from")
    @patch("os.path.isdir")
    @patch("os.makedirs")
    def test_retrieveVersionsByGitHash_BuildVersionToCommitHashDictionary(self, makedirs_mock, isdir_mock, clone ):
        isdir_mock.return_value = False
        repo_mock = MagicMock()
        clone.return_value = repo_mock

        tag1 = MagicMock();
        tag1.commit = "23a1f23h"
        tag1.__str__.return_value = "origin/tags/1.2.3.4"

        tag2 = MagicMock();
        tag2.commit = "13a1f13h"
        tag2.__str__.return_value = "origin/tags/4.2.1.3"

        repo_mock.tags = [ tag1, tag2 ]
        repo_mock.remotes["origin"] = Mock()
        conf = { "Directory" : "testDir", "RepositoryUrl" : "git://some.url/repo.git" }
        repo = GitRepo.GitRepo(conf)
        repo.checkout();
        repo.retrieveVersionsByGitHash([])

        self.assertEqual("1.2.3.4", repo.versionsByGitHash["23a1f23h"]);
        self.assertEqual("4.2.1.3", repo.versionsByGitHash["13a1f13h"]);

if __name__ == '__main__':
    unittest.main()
