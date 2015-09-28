import unittest
from JustReleaseNotes.sourcers import GitRepo
from mock import Mock, MagicMock, mock_open, patch

class Commit:

    def __init__(self, hexsha):
        self.hexsha = hexsha
        self.parents = []
        self.summary = ""
        self.message = ""
        self.authored_date = ""

class GitRepo_Test(unittest.TestCase):

    def method_throws(*args, **kwargs):
        raise Exception("Error")

    @patch("git.Repo.clone_from")
    def test_GitRepoSetsTheRemoteAndBranch(self, repo_mock):
        conf = { "Directory" : "testDir", "Branch" : "origin/release/1.2.0" ,"RepositoryUrl" : "git://some.url/repo.git" }
        mock = MagicMock()
        mock.create_head = Mock()
        repo_mock.return_value = mock
        repo = GitRepo.GitRepo(conf)
        repo.checkout()
        mock.create_head.assert_called_once_with("release/1.2.0", "origin/release/1.2.0")
        repo.checkout()

    @patch("git.Repo.clone_from")
    @patch("git.Repo.iter_commits")
    def test_retrieveHistoryProcessesEachCommit(self, iter_commits, repo_mock):
        commit1 = Commit("1")
        commit2 = Commit("2")
        commit3 = Commit("3")
        iter_commits.return_value = [commit1, commit3, commit2]
        mock = MagicMock()
        mock.iter_commits = iter_commits
        repo_mock.return_value = mock
        conf = { "Directory" : "testDir", "RepositoryUrl" : "git://some.url/repo.git" }
        repo = GitRepo.GitRepo(conf)
        repo.checkout()
        repo.retrieveHistory()
        self.assertIn("1", repo.gitCommitMessagesByHash)
        self.assertIn("1", repo.gitCommitsList)
        self.assertIn("1", repo.gitDatesByHash)
        self.assertIn("2", repo.gitCommitMessagesByHash)
        self.assertIn("2", repo.gitCommitsList)
        self.assertIn("2", repo.gitDatesByHash)
        self.assertIn("3", repo.gitCommitMessagesByHash)
        self.assertIn("3", repo.gitCommitsList)
        self.assertIn("3", repo.gitDatesByHash)

    def test_setParentsTraersesChildrenAndDelasWithCycles(self):
        conf = { "Directory" : "testDir", "RepositoryUrl" : "git://some.url/repo.git" }
        repo = GitRepo.GitRepo(conf)
        commit = Commit("32423424af")
        commit.message = "test message"
        commit.summary = "some summary"
        commit.authored_date = ""
        commit.parents = [ ]
        repo.processCommit(commit)
        self.assertIn("32423424af", repo.gitCommitMessagesByHash)
        self.assertIn("32423424af", repo.gitCommitsList)
        self.assertIn("32423424af", repo.gitDatesByHash)

    def test_setParentsTraersesChildrenAndDelasWithCycles(self):
        conf = { "Directory" : "testDir", "RepositoryUrl" : "git://some.url/repo.git" }
        repo = GitRepo.GitRepo(conf)
        commit = Commit("32423424af")
        child = Commit("1")
        child.parents = [commit]
        commit.parents = [ child, Commit("2") ]
        repo.setParents(commit)
        self.assertEqual(2, len(repo.commitParents["32423424af"]))
        self.assertIn("32423424af", repo.commitParents)


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
