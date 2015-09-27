import unittest
from mock import Mock
from JustReleaseNotes.writers import StashMarkdownWriter

class StashMarkdownWriter_Test(unittest.TestCase):

    def test_givenFairlyCompleteTicketMarkdownBlockIsGenerated(self):
        mockedTicketProvider = Mock()
        writer = StashMarkdownWriter.StashMarkdownWriter(mockedTicketProvider)
        self.assertEqual("", writer.getImageBlock("http://icon.url/image.png"));


if __name__ == '__main__':
    unittest.main()