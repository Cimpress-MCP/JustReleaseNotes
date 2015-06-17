import unittest
from JustReleaseNotes.sourcers import GitRepo
from mock import patch

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

if __name__ == '__main__':
    unittest.main()
