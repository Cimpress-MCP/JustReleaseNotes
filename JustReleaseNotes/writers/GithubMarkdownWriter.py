from JustReleaseNotes.writers import MarkdownWriter

class GithubMarkdownWriter(MarkdownWriter.MarkdownWriter):

    def __init__(self, ticketProvider):
        MarkdownWriter.MarkdownWriter.__init__(self, ticketProvider)

    def getImageBlock(self, icon):
        return "<img src=\"{0}\" width=16 height=16></img>".format(icon)
