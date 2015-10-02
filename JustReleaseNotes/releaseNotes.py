from datetime import datetime


class ReleaseNotes:

    __PendingPromotionCaption = "Pending promotion"
    __conf = {}
    __promotedVersionsInfo = {}
    __ticketProvider = {}
    __fromDate = 0

    def __init__(self, conf, ticketProvider, repo, promotedVersionsInfo):
        self.__conf = conf
        self.__repo = repo
        self.__promotedVersionsInfo = promotedVersionsInfo
        self.__ticketProvider = ticketProvider

        self.__repo.checkout()
        self.__repo.retrieveHistory()
        self.__repo.retrieveVersionsByGitHash(list(self.__promotedVersionsInfo.keys()))

        if "OldestCommitToProcess" in conf["Source"]:
            oldestCommitToProcess = conf["Source"]["OldestCommitToProcess"]
            self.__fromDate = self.__repo.gitDatesByHash[oldestCommitToProcess]

    def __printVersionBlock(self, version, tickets, writer):
        date = "N/A"
        deps = {}
        if version != self.__PendingPromotionCaption:
            if version in self.__promotedVersionsInfo:
                date = self.__promotedVersionsInfo[version]["date"]
                if "directDependencies" in self.__promotedVersionsInfo[version]:
                    deps = self.__promotedVersionsInfo[version]["directDependencies"]

        if len(tickets) == 0:
            return ""

        return writer.printVersionBlock(deps, version, date, tickets)

    def generateReleaseNotesByPromotedVersions(self, writer):
        
        ticketsSoFar = []
        hashesInVersion = self.__repo.gitHistoryByVersion

        hashAlreadySeen = []
        sortedVersions = [] + list(hashesInVersion.keys())
        sortedVersions.sort(key=lambda s: list(map(int, s.split('.'))))
        
        content = []
        for version in sortedVersions:

            if version in self.__promotedVersionsInfo or len(self.__promotedVersionsInfo.keys()) == 0:
                print("Generating info for version " + version)
                
            for hash in hashesInVersion[version]:
                if self.__repo.gitDatesByHash[hash] < self.__fromDate:
                    continue
                if hash in hashAlreadySeen:
                    continue
                hashAlreadySeen = hashAlreadySeen + [hash]

                ticketsSoFar += self.__ticketProvider.extractTicketsFromMessage(self.__repo.gitCommitMessagesByHash[hash])

            if version in self.__promotedVersionsInfo or len(self.__promotedVersionsInfo.keys()) == 0:
                content = [self.__printVersionBlock(version, ticketsSoFar, writer)] + content
                ticketsSoFar = []                

        if len(ticketsSoFar) > 0:
            content = [self.__printVersionBlock(self.__PendingPromotionCaption, ticketsSoFar, writer)] + content

        return "\n".join(content).strip(' \t\n\r')
