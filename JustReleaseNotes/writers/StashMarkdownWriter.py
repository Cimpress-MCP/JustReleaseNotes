from JustReleaseNotes.writers import MarkdownWriter

class StashMarkdownWriter(MarkdownWriter.MarkdownWriter):

    def __init__(self, ticketProvider):
        MarkdownWriter.MarkdownWriter.__init__(self, ticketProvider)

    def getImageBlock(self, icon):
        return ""
