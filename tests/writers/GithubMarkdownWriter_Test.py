import unittest
from mock import Mock
from JustReleaseNotes.writers import GithubMarkdownWriter

class StashMarkdownWriter_Test(unittest.TestCase):

    def test_givenFairlyCompleteTicketMarkdownBlockIsGenerated(self):
        mockedTicketProvider = Mock()
        writer = GithubMarkdownWriter.GithubMarkdownWriter(mockedTicketProvider)
        self.assertEqual("<img src=\"http://icon.url/image.png\" width=16 height=16></img>",
                         writer.getImageBlock("http://icon.url/image.png"));


if __name__ == '__main__':
    unittest.main()