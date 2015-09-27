import re
import sys

class BaseWriter:

    def __init__(self, ticketProvider):
        self.ticketProvider = ticketProvider
        self.versionsAlreadyPresent = {}
        self.__upcomingDevelopments = "Upcoming developments"

    def convertVersion(self, version):
        if (version == str(sys.maxsize)):
            version = self.__upcomingDevelopments
        return version

    def deconvertVersion(self, version):
        if (version == self.__upcomingDevelopments):
            version = str(sys.maxsize)
        return version

    def parseVersionHeader(self, line):
        return False

    def setInitialContent(self, content):
        currentVersion = None
        for line in content.split("\n"):
            v = self.deconvertVersion(self.parseVersionHeader(line))
            if v is not False and v != str(sys.maxsize):
                currentVersion = v
                self.versionsAlreadyPresent[v] = []
            if currentVersion is not None:
                self.versionsAlreadyPresent[currentVersion].append(line)
        return self.versionsAlreadyPresent

    def printVersionBlock(self, deps, version, date, tickets):
        if version in self.versionsAlreadyPresent.keys():
            return '\n'.join(self.versionsAlreadyPresent[version]);
        return None
