import re

class HtmlWriter:

    def __init__(self, ticketProvider):
        self.__ticketProvider = ticketProvider

    def getExtension(self):
        return ".html"

    def printVersionBlock(self, version, date, tickets):
        data = [
            "<div style=\"width:100%; border: 0px\">",
            "<a name=\"" + version + "\"></a>",
            "<h2>" + version + "<sup><small style=\"font-size:10px\"><i> " + date + "</i></small></sup></h2>",
            ]

        uniqTickets = sorted(set(tickets), reverse=True)
        for ticket in uniqTickets:
            if ticket == "NULL":
                data.append("<li style=\"font-size:14px\">Stability improvements</li>")
            else:
                ticketInfo = self.__ticketProvider.getTicketInfo(ticket)
                if ticketInfo != None:
                    title = ticketInfo["title"]
                    if "embedded_link" in ticketInfo:
                        for ticket, link in ticketInfo["embedded_link"].iteritems():
                            title = re.sub(ticket, "<a href='{0}'>{1}</a>".format(link, ticket), title)
                    data.append('<li style="font-size:14px"><img src="{1}" alt="{0}" width="16" height="16" style="padding-right: 5px"></img><a href="{4}">{2}</a> {3}</li>'.format("state", ticketInfo["state_icon"], ticketInfo["ticket"], title , ticketInfo["html_url"]))

        data += ["</ul>", "</div>", ""]

        return '\n'.join(data)