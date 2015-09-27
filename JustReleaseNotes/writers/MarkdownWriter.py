import re
import sys
from JustReleaseNotes.writers import BaseWriter

class MarkdownWriter(BaseWriter.BaseWriter):

    def __init__(self, ticketProvider):
        BaseWriter.BaseWriter.__init__(self, ticketProvider)

    def getExtension(self):
        return ".md"

    def getImageBlock(self, icon):
        return "![Icon]({0})".format(icon)

    def getVersionHeader(self, version):
        return "## {0} ##".format(version)

    def parseVersionHeader(self, line):
        if (line.startswith("## ") and line.endswith(" ##")):
            return line[3:len(line)-3]
        else:
            return False

    def printVersionBlock(self, deps, version, date, tickets):
        baseoutput = BaseWriter.BaseWriter.printVersionBlock(self, deps, version, date, tickets)
        if baseoutput is not None:
            return baseoutput

        version = self.convertVersion(version)
        data = [self.getVersionHeader(version)]
        if date != 'N/A':
            data.append(date)

        data.append("")
        uniqTickets = sorted(set(tickets), reverse=True)
        appendStabilityImprovements = False;

        for ticket in uniqTickets:
            if ticket == "NULL":
                appendStabilityImprovements = True
            else:
                ticketInfo = self.ticketProvider.getTicketInfo(ticket)
                if ticketInfo != None:
                    title = ticketInfo["title"]
                    if "embedded_link" in ticketInfo:
                        for ticket, link in list(ticketInfo["embedded_link"].items()):
                            title = re.sub(ticket, "[{1}]({0})".format(link, ticket), title)
                    iconPart = ""
                    if "issue_type_icon" in ticketInfo:
                        iconPart = self.getImageBlock(ticketInfo["issue_type_icon"])
                    data.append("* {0} [{1}]({3}) {2}, *reported by* **{4}**".format(iconPart, ticketInfo["ticket"],
                                                              title.encode('ascii','ignore').decode("ascii") ,
                                                              ticketInfo["html_url"],
                                                              ticketInfo["reporter"]))

        if appendStabilityImprovements:
            data.append("* Stability improvements")

        return '\n'.join(data) + '\n'