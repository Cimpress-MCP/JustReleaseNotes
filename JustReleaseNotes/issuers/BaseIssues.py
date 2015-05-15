import re

class BaseIssues():

    ticketRegex = None

    def extractTicketsFromMessage(self, message):
        message = message.replace("\n", " ").replace("\r", " ").replace("\t", " ");
        p = re.compile(self.ticketRegex)
        results = p.findall(message)
        if len(results) > 0:
            return results
        else:
            return ["NULL"]