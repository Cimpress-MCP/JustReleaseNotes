import re

class MarkdownWriter:

    def __init__(self, ticketProvider):
        self.__ticketProvider = ticketProvider

    def getExtension(self):
        return ".md"

    def printVersionBlock(self, version, date, tickets):
        data = ["## {0} ##".format(version), date, ""]

        uniqTickets = sorted(set(tickets), reverse=True)

        for ticket in uniqTickets:
            if ticket == "NULL":
                data.append("* Stability improvements")
            else:
                ticketInfo = self.__ticketProvider.getTicketInfo(ticket)
                if ticketInfo != None:
                    title = ticketInfo["title"]
                    for ticket, link in ticketInfo["embedded_link"].iteritems():
                        title = re.sub(ticket, "[{1}]({0})".format(link, ticket), title)
                    data.append("* " + "![{0}]({1}) [{2}]({4}) {3}".format("state", ticketInfo["state_icon"], ticketInfo["ticket"], title, ticketInfo["html_url"]) )

        return '\n'.join(data)