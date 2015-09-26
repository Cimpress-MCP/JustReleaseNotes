import sys
import requests
import json
from JustReleaseNotes.issuers import BaseIssues

class GitHubIssues(BaseIssues.BaseIssues):
    __conf = None
    __cache = {}
    
    def __init__(self, conf):
        self.__conf = conf
        self.__iconMappings = dict(
            issue="http://www.ic.gc.ca/app/opic-cipo/trdmrks/srch/imageLoader?appNum=1366861&extension=",
            pull_request="https://addons.cdn.mozilla.net/user-media/addon_icons/603/603460-64.png?modified=1428920625")
        self.ticketRegex = '#([0-9]+)'
        if "TicketRegex" in conf:
            self.ticketRegex = conf["TicketRegex"]

        headers = { 'Authorization': self.__conf["Authorization"] }
        response = requests.get( self.__conf["Url"] + "?filter=all&state=all", headers = headers, verify=False )
        tickets = json.loads(response.text)

        for ticketData in tickets:
            ticketNumber = str(ticketData["number"])
            self.__cache[ticketNumber] = ticketData

    def __log(self, message):
        print ("GitHub Issues: " + message)
        sys.stdout.flush()
        
    def __readJsonInfo(self, ticket):

        if ticket in self.__cache.keys():
            self.__log("Cached ticket info for " + ticket)
            return self.__cache[ticket]
        else:
            uri = self.__conf["Url"] + "/" + ticket
            self.__log("Retrieving ticket info for {0}: {1}".format(ticket, uri))

            headers = { 'Authorization': self.__conf["Authorization"] }
            r = requests.get( uri, headers = headers, verify=False )

            data = json.loads(r.text)
            if "message" in data and data["message"] == "Not Found":
                self.__log("Error retrieving GitHub Issue info: " + data["message"])
            self.__cache[ticket] = data
            return data

    def getTicketInfo(self, ticket):
        data = self.__readJsonInfo(ticket)

        if "title" in data:
            title = data["title"]
            embedded_links = {}
            for t in self.extractTicketsFromMessage(title):
                embedded_links["#" + t] = "{0}/{1}".format(self.__conf["HtmlUrl"], t)
        else:
            title = "Untitled"

        if "pull_request" in data:
            issueType = "pull_request"
        else:
            issueType = "issue"

        return { "issue_type_icon" : self.__iconMappings[issueType],
            "html_url" : data["html_url"],
            "ticket" : "#{0}".format(ticket),
            "title" : title,
            "embedded_link" : embedded_links,
            "reporter": data["user"]["login"]}

