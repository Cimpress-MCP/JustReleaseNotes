import re
from JustReleaseNotes.writers import BaseWriter

class MarkdownWriter(BaseWriter.BaseWriter):

    def __init__(self, ticketProvider):
        self.__ticketProvider = ticketProvider

    def getExtension(self):
        return ".md"

    def getImageBlock(self, icon):
        return "![Icon]({0})".format(icon)

    def printVersionBlock(self, deps, version, date, tickets):
        version = self.convertVersion(version)

        data = ["## {0} ##".format(version)]
        if date != 'N/A':
            data.append(date)

        data.append("")
        uniqTickets = sorted(set(tickets), reverse=True)
        appendStabilityImprovements = False;

        for ticket in uniqTickets:
            if ticket == "NULL":
                appendStabilityImprovements = True
            else:
                ticketInfo = self.__ticketProvider.getTicketInfo(ticket)
                if ticketInfo != None:
                    title = ticketInfo["title"]
                    if "embedded_link" in ticketInfo:
                        for ticket, link in list(ticketInfo["embedded_link"].items()):
                            title = re.sub(ticket, "[{1}]({0})".format(link, ticket), title)
                    iconPart = ""
                    if "issue_type_icon" in ticketInfo:
                        iconPart = self.getImageBlock(ticketInfo["issue_type_icon"])
                    data.append("* {0} [{1}]({3}) {2}".format(iconPart, ticketInfo["ticket"], title.encode('ascii','ignore').decode("ascii") , ticketInfo["html_url"]) )

        if appendStabilityImprovements:
            data.append("* Stability improvements")

        return '\n'.join(data) + '\n'