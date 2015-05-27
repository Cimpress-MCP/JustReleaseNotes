class ReleaseNotes:

    __PendingPromotionCaption = "Pending promotion"
    __Writer = "MarkdownWriter"
    __conf = {}
    __ticketsByVersion = {}
    __promotedVersionsInfo = {}
    __ticketReplacements = {}
    __ticketProvider = {}

    def __init__(self, conf, ticketProvider, releaseNotesWriter, repo, promotedVersionsInfo):
        self.__ticketsByVersion = {}
        self.__conf = conf
        self.__Writer = releaseNotesWriter
        self.__repo = repo
        self.__promotedVersionsInfo = promotedVersionsInfo
        self.__ticketProvider = ticketProvider;
        
    def __computeTicketsByVersion(self):
        currentVersion = "latest"        
        self.__ticketsByVersion[currentVersion] = []
        for hash in self.__repo.gitCommitsList:
            if hash in self.__repo.versionsByGitHash:
                currentVersion = self.__repo.versionsByGitHash[hash]
                self.__ticketsByVersion[currentVersion] = []
            tickets = self.__ticketProvider.extractTicketsFromMessage(self.__repo.gitCommitMessagesByHash[hash])
            self.__ticketsByVersion[currentVersion] = self.__ticketsByVersion[currentVersion] + tickets
     
    def __printVersionBlock(self, version, tickets):        
        date = "N/A"
        deps = {}
        if version != self.__PendingPromotionCaption:
            if version in self.__promotedVersionsInfo:
                date = self.__promotedVersionsInfo[version]["date"]
                if "directDependencies" in self.__promotedVersionsInfo[version]:
                    deps = self.__promotedVersionsInfo[version]["directDependencies"]

        if len(tickets) == 0:
            return ""
        return self.__Writer.printVersionBlock(deps, version, date, tickets)

    def generateReleaseNotesByPromotedVersions(self):
        
        self.__repo.checkout()
        self.__repo.retrieveHistory()
        self.__repo.retrieveVersionsByGitHash( list(self.__promotedVersionsInfo.keys()) )
        self.__computeTicketsByVersion()

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
                if hash in hashAlreadySeen:
                    continue
                hashAlreadySeen = hashAlreadySeen + [hash]
                if hash not in self.__repo.gitCommitMessagesByHash:
                    self.__repo.processCommit(hash)
                ticketsSoFar += self.__ticketProvider.extractTicketsFromMessage(self.__repo.gitCommitMessagesByHash[hash])

            if version in self.__promotedVersionsInfo or len(self.__promotedVersionsInfo.keys()) == 0:
                content = content + [self.__printVersionBlock(version, ticketsSoFar)]
                ticketsSoFar = []                

        if len(ticketsSoFar) > 0:
            content = content + [self.__printVersionBlock(self.__PendingPromotionCaption, ticketsSoFar)]           
        
        content.sort(reverse=True)        
        return "\n".join(content)
