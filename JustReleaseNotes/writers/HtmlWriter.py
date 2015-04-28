import re

class HtmlWriter:

    def __init__(self, ticketProvider):
        self.__ticketProvider = ticketProvider

    def getExtension(self):
        return ".html"

    def printVersionBlock(self, deps, version, date, tickets):
        data = [
            "<div style=\"width:100%; border: 0px\">",
            "<a name=\"" + version + "\"></a>"]

        data.append("<h2>" + version)
        if date != 'N/A':
            data.append("<sup><small style=\"font-size:10px\"><i> " + date + "</i></small></sup>")
        data.append("</h2>")

        if len(deps.keys()) > 0:
            data.append('<div style="background: #eee; "><i>Components: ')
            data.append('; '.join(deps.values()))
            data.append('</i></div>')

        data.append("<ul>")
        uniqTickets = sorted(set(tickets), reverse=True)

        appendStabilityImprovements = False

        for ticket in uniqTickets:
            if ticket == "NULL":
                appendStabilityImprovements = True
            else:
                ticketInfo = self.__ticketProvider.getTicketInfo(ticket)
                if ticketInfo != None:
                    title = ticketInfo["title"]
                    if "embedded_link" in ticketInfo:
                        for ticket, link in ticketInfo["embedded_link"].iteritems():
                            title = re.sub(ticket, "<a href='{0}'>{1}</a>".format(link, ticket), title)
                    imgFormat = '<img src="{1}" alt="{0}" width="16" height="16" style="padding-right: 5px"></img>'
                    imgHtml = ""
                    if "state_icon" in ticketInfo:
                        imgHtml += imgFormat.format("State", ticketInfo["state_icon"])
                    if "issue_type_icon" in ticketInfo:
                        imgHtml += imgFormat.format("Issue Type", ticketInfo["issue_type_icon"])
                    if "priority_icon" in ticketInfo:
                        imgHtml += imgFormat.format("Priority", ticketInfo["priority_icon"])
                    data.append('<li style="font-size:14px">{0}<a href="{3}">{1}</a> {2}</li>'.format(imgHtml, ticketInfo["ticket"], title , ticketInfo["html_url"]))

        if appendStabilityImprovements:
            data.append("<li style=\"font-size:14px\">Stability improvements</li>")

        data += ["</ul>", "</div>", ""]

        return '\n'.join(data)