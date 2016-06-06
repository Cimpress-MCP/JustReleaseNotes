import json
from JustReleaseNotes.writers import BaseWriter

class JsonWriter(BaseWriter.BaseWriter):

    def __init__(self, ticketProvider):
        BaseWriter.BaseWriter.__init__(self, ticketProvider)

    def getExtension(self):
        return ".json"

    def setInitialContent(self, content):
        # expected format of full JSON:
        # { [ "version": "version 1", "tickets": { ... }, "version": "version 2", "tickets": { ... } ] }
        # this hashes the content with the version, but leaves the whole blob per version as content
        data = json.loads(content) if content != "" else []
        self.versionsAlreadyPresent = dict((x["version"], x) for x in data)
        return self.versionsAlreadyPresent

    def printVersionBlock(self, deps, version, date, tickets):

        # get the content of a specific version if already present
        if version in self.versionsAlreadyPresent.keys():
            return json.dumps(self.versionsAlreadyPresent[version])

        # sort the ticket
        uniqTickets = sorted(set(tickets), reverse=True)
        appendStabilityImprovements = False;

        # default version
        ticketsInThisVersion = self.versionsAlreadyPresent.get(version, [])

        # append the tickets for this version
        for ticket in uniqTickets:
            if ticket == "NULL":
                appendStabilityImprovements = True
            else:
                ticketsInThisVersion.append(self.ticketProvider.getTicketInfo(ticket))

        # also append a default ticket for stability improvements if not ticket could be found
        if appendStabilityImprovements:
            ticketsInThisVersion.append({"title": "Stability Improvements"})

        # the entry contains the version and the tickets, which is serialized into a string
        entry = {"version": version, "tickets": ticketsInThisVersion}
        self.versionsAlreadyPresent[version] = entry
        block = json.dumps(entry)
        return block

    # overrides the default behavior of generating the document since we need valid JSON
    def writeDocument(self, content):
        versions = ",".join(content).strip()
        return "[" + versions + "]"