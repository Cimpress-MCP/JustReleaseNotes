import os, sys, re, subprocess
import requests
import json
import getpass

class HtmlWriter:

    def __init__(self, ticketProvider):
        self.__ticketProvider = ticketProvider

    def getExtension(self):
        return ".html"

    def printVersionBlock(self, version, deps, date, tickets):
        data = [
            "<div style=\"width:100%; border: 0px\">",
            "<a name=\"" + version + "\"></a>",
            "<h2>" + version + "<sup><small style=\"font-size:10px\"><i> " + date + "</i></small></sup></h2>",
            ]

        d = []
        for item in list(deps.keys()):
            if item in self.__conf["DirectDependenciesInfo"]:
                d.append( '<a href="{2}#{1}">{0} {1}</a>'.format(
                    item, deps[item],
                    self.__conf["DirectDependenciesInfo"][item]["WikiPageTitle"]))
            else:
                if item == "ANY":
                    d.append(deps[item])
                else:
                    d.append( '{0} {1}'.format(item, deps[item]))

        if len(d) > 0:
            data.append('<div style="background: #eee; "><i>Components: ')
            data.append('; '.join(d))
            data.append('</i></div>')

        data.append("<ul>")
        uniqTickets = sorted(set(tickets), reverse=True)

        for ticket in uniqTickets:
            ticketInfo = self.__ticketProvider.getTicketInfo(ticket)
            if ticket == "NULL":
                data.append("<li style=\"font-size:14px\">Stability improvements</li>")
            else:
                title = ticketInfo["title"]
                for ticket, link in ticketInfo["embedded_link"].iteritems():
                    title = re.sub(ticket, "<a href='{0}'>{1}</a>".format(link, ticket), title)
                data.append('<li style="font-size:14px"><img src="{1}" alt="{0}"></img><a href="{4}">#{2}</a> {3}</li>'.format("state", ticketInfo["state_icon"],  ticketInfo["ticket"], title , ticketInfo["html_url"]))

        data = data + ["</ul>", "</div>", ""]

        return '\n'.join(data)