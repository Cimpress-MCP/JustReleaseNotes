class WikiWriter:

    def __init__(self, ticketProvider):
        self.__ticketProvider = ticketProvider

    def getExtension(self):
        return ".wiki"

    def printVersionBlock(self, version, deps, date, tickets):
        lines = [
            "<div class=\"mw-collapsible\" style=\"width:100%; border: 0px\">",
            "<big>'''" + version + "'''" + " (Date: " + date + ")</big>",
            "<div class=\"mw-collapsible-content\">",
            ]

        uniqTickets = sorted( set(tickets), reverse=True)
        for ticket in uniqTickets:
            if ticket == "NULL":
                lines.append("* Stability improvements")
            else:
                lines.append("* {{JiraTrain with summary |" + ticket + "}}")

        return '\n'.join(lines + [ "</div>", "</div>", "<hr>" ])