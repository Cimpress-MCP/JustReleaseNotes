import re
from JustReleaseNotes.writers import BaseWriter

class HtmlWriter(BaseWriter.BaseWriter):

    def __init__(self, ticketProvider):
        BaseWriter.BaseWriter.__init__(self, ticketProvider)

    def getExtension(self):
        return ".html"

    def getVersionHeader(self, version):
        return "<div style=\"width:100%; border: 0px\"><a name=\"{0}\" class=\"version\"></a>".format(version)

    def parseVersionHeader(self, line):
        if (line.startswith("<div style=\"width:100%; border: 0px\"><a name=\"") and line.endswith("\" class=\"version\"></a>")):
            return line[46:len(line)-22]
        else:
            return False


    def printVersionBlock(self, deps, version, date, tickets):
        baseoutput = BaseWriter.BaseWriter.printVersionBlock(self, deps, version, date, tickets)
        if baseoutput is not None:
            return baseoutput

        version = self.convertVersion(version)

        data = [self.getVersionHeader(version), "<h2>" + version]

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
                ticketInfo = self.ticketProvider.getTicketInfo(ticket)
                if ticketInfo != None:
                    title = ticketInfo["title"]
                    if "embedded_link" in ticketInfo:
                        for ticket, link in list(ticketInfo["embedded_link"].items()):
                            title = re.sub(ticket, "<a href=\"{0}\">{1}</a>".format(link, ticket), title)
                    imgFormat = '<img src="{1}" alt="{0}" width="16" height="16" style="padding-right: 5px"></img>'
                    imgHtml = ""
                    if "state_icon" in ticketInfo:
                        imgHtml += imgFormat.format("State", ticketInfo["state_icon"])
                    if "issue_type_icon" in ticketInfo:
                        imgHtml += imgFormat.format("Issue Type", ticketInfo["issue_type_icon"])
                    if "priority_icon" in ticketInfo:
                        imgHtml += imgFormat.format("Priority", ticketInfo["priority_icon"])
                    data.append('<li style="font-size:14px">{0}<a href="{3}">{1}</a> {2}, <i>reported by</i> <b>{4}</b></li>'.format(
                        imgHtml, ticketInfo["ticket"], title , ticketInfo["html_url"], ticketInfo["reporter"]))

        if appendStabilityImprovements:
            data.append("<li style=\"font-size:14px\">Stability improvements</li>")

        data += ["</ul>", "</div>", ""]

        return '\n'.join(data)