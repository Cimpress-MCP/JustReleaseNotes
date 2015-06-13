import sys
import JustReleaseNotes
from JustReleaseNotes.issuers import BaseIssues

class AggregateIssuer(BaseIssues.BaseIssues):
    __conf = None
    __issuers = {}
    
    def __init__(self, issuersConfArray):
        self.__issuers = []
        for issuerConf in issuersConfArray:
            issuer = JustReleaseNotes.issuers.factory.create(issuerConf)
            self.__issuers.append(issuer)

    def extractTicketsFromMessage(self, message):
        ret = []
        for issuer in self.__issuers:
            ret.extend(issuer.extractTicketsFromMessage(message))
        return ret

    def getTicketInfo(self, ticket):
        for issuer in self.__issuers:
            if issuer.extractTicketsFromMessage(ticket) != ["NULL"]:
                return issuer.getTicketInfo(ticket)
        return None
