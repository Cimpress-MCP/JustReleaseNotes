import sys, re
import requests
import json
from JustReleaseNotes.issuers import BaseIssues

class JiraIssues(BaseIssues.BaseIssues):
    __restSearchUrl = None
    __jiraAuthorization = None
    __cache = {}

    def __init__(self, conf):
        self.__restSearchUrl = conf["Url"]
        self.__jiraAuthorization = conf["Authorization"]
        self.__conf = conf
        self.ticketRegex = '([A-Z]{2,5}-[0-9]+)'
        if "TicketRegex" in conf:
            self.ticketRegex = conf["TicketRegex"]

    def __log(self, message):
        print ("Jira: " + message)
        sys.stdout.flush()

    def __readJsonInfo(self, ticket):

        if ticket in self.__cache:
            self.__log("Cached ticket info for " + ticket)
            return self.__cache[ticket]

        uri = "{0}/{1}".format(self.__restSearchUrl,ticket)
        headers = { 'Authorization': self.__jiraAuthorization }
        self.__log("Retrieving ticket info for " + ticket)
        r = requests.get( uri, headers = headers, verify=False )
        data = json.loads(r.text)
        if "errorMessages" in data:
            self.__log("Error retrieving Jira info: " + ",".join(data["errorMessages"]))
        self.__cache[ticket] = data
        return data

    def getTicketInfo(self, ticket):
        data = self.__readJsonInfo(ticket)

        embedded_links = {}
        title = "Untitled"
        ret = { "html_url" : "{0}/{1}".format(self.__conf["HtmlUrl"],ticket),
                "ticket" : ticket,
                "title" : title }

        if "fields" in data.keys():
            title = data["fields"]["summary"]
            ret["title"] = title
            for ticket in self.extractTicketsFromMessage(title):
                embedded_links[ticket] = "{0}/{1}".format(self.__conf["HtmlUrl"],ticket)
            ret["state_icon"] = self.__fieldIcon(data["fields"]["status"])
            ret["issue_type_icon"] = self.__fieldIcon(data["fields"]["issuetype"])
            ret["priority_icon"] = self.__fieldIcon(data["fields"]["priority"])
            ret["embedded_link"] = embedded_links
            ret["reporter"] = data["fields"]["reporter"]["displayName"]
        else:
            return None

        return ret

    def __fieldIcon(self, f):
        if "WebImagesPath" in self.__conf:
            parts = f["iconUrl"].split("/")
            return '{0}/{1}'.format(self.__conf["WebImagesPath"], parts[len(parts)-1], f["name"])
        else:
            return f["iconUrl"]
