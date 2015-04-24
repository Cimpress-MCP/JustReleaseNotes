import os, sys, re, subprocess
import requests
import json
import getpass

class JiraIssues:
    __restSearchUrl = None
    __jiraAuthorization = None
    __cache = {}

    def __init__(self, conf):
        self.__restSearchUrl = conf["JiraRestSearchUrl"]
        self.__jiraAuthorization = conf["Authorization"]

    def __log(self, message):
        print ("Jira: " + message)
        sys.stdout.flush()

    def __readJsonInfo(self, ticket):

        if ticket in self.__cache:
            self.__log("Cached ticket info for " + ticket)
            return self.__cache[ticket]

        uri = self.__restSearchUrl + ticket
        headers = { 'Authorization': self.__jiraAuthorization }
        self.__log("Retrieving ticket info for " + ticket)
        r = requests.get( uri, headers = headers, verify=False )
        data = json.loads(r.text)
        if "errorMessages" in data:
            self.__log("Error retrieving Jira info: " + data["errorMessages"])
        self.__cache[ticket] = data
        return data

    def printTicketInfo(self, ticket):
        data = self.__readJsonInfo(ticket)

        r = [
            self.__fieldIcon(data["fields"]["issuetype"]),
            self.__fieldIcon(data["fields"]["status"]),
            self.__fieldIcon(data["fields"]["priority"]),
            '<a href="{0}{1}" class="extiw">{1}</a>'.format(self.__conf["JiraConf"]["JiraBrowseUrl"], ticket),
            data["fields"]["summary"],
            ]

        return ' '.join(r) + '\n'

