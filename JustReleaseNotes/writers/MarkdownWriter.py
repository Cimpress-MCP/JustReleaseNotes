import re

class MarkdownWriter:

    def __init__(self, ticketProvider):
        self.__ticketProvider = ticketProvider

    def getExtension(self):
        return ".md"

    def printVersionBlock(self, deps, version, date, tickets):
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
                        iconPart = "<img src=\"{0}\" width=16 height=16></img>".format(ticketInfo["issue_type_icon"])
                    data.append("* {0} [{1}]({3}) {2}".format(iconPart, ticketInfo["ticket"], title.encode('ascii','ignore'), ticketInfo["html_url"]) )

        if appendStabilityImprovements:
            data.append("* Stability improvements")

        return '\n'.join(data) + '\n'