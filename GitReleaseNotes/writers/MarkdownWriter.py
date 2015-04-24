import os, sys, re, subprocess
import requests
import json
import getpass

class MarkdownWriter:

    def __init__(self, ticketProvider):
        self.__ticketProvider = ticketProvider

    def getExtension(self):
        return ".md"

    def printVersionBlock(self, version, deps, date, tickets):
        data = ["## {0} ##".format(version)]
        d = []

        for item in list(deps.keys()):
            if item == "ANY":
                d.append(deps[item])
            else:
                d.append( '{0} {1}'.format(item, deps[item]))

        if len(d) > 0:
            data.append('Components: ')
            data.append('; '.join(d))
            data.append('')

        uniqTickets = sorted(set(tickets), reverse=True)

        for ticket in uniqTickets:
            if ticket == "NULL":
                data.append("* Stability improvements")
            else:
                ticketInfo = self.__ticketProvider.getTicketInfo(ticket)
                title = ticketInfo["title"]
                for ticket, link in ticketInfo["embedded_link"].iteritems():
                    title = re.sub(ticket, "[{1}]({0})".format(link, ticket), title)
                data.append("* " + "![{0}]({1}) [#{2}]({4}) {3}".format("state", ticketInfo["state_icon"],  ticketInfo["ticket"], title, ticketInfo["html_url"]) )

        data = data

        return '\n'.join(data)