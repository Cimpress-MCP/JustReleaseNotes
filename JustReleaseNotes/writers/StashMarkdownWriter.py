from JustReleaseNotes.writers import MarkdownWriter

class StashMarkdownWriter(MarkdownWriter.MarkdownWriter):

    def __init__(self, ticketProvider):
        super(StashMarkdownWriter, self).__init__(ticketProvider)

    def getImageBlock(self, icon):
        return ""
