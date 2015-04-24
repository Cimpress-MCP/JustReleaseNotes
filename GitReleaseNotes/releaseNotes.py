from gitrepo import *

class ReleaseNotes:

    __PendingPromotionCaption = "Pending promotion"
    __Writer = "MarkdownWriter"
    __conf = {}
    __ticketsByVersion = {}
    __promotedVersionsInfo = {}
    __ticketReplacements = {}
    __ticketProvider = {}

    def __init__(self, conf, ticketProvider, releaseNotesWriter, git, promotedVersionsInfo):
        self.__ticketsByVersion = {}
        self.__conf = conf
        if "PendingPromotionCaption" in conf:
            self.__PendingPromotionCaption = conf["PendingPromotionCaption"]

        self.__Writer = releaseNotesWriter
        self.__git = git
        self.__promotedVersionsInfo = promotedVersionsInfo
        
        self.__ticketReplacements = {}
        if "TicketReplacements" in conf:
            self.__ticketReplacements = conf["TicketReplacements"]

        self.__ticketProvider = ticketProvider;
        
    def __computeTicketsByVersion(self):
        currentVersion = "latest"        
        self.__ticketsByVersion[currentVersion] = []
        for hash in self.__git.gitCommitsList:
            if hash in self.__git.versionsByGitHash:
                currentVersion = self.__git.versionsByGitHash[hash] 
                self.__ticketsByVersion[currentVersion] = []
            tickets = self.__ticketProvider.extractTicketsFromMessage(self.__git.gitCommitMessagesByHash[hash])
            self.__ticketsByVersion[currentVersion] = self.__ticketsByVersion[currentVersion] + tickets     
     
    def __printVersionBlock(self, version, tickets):        
        date = "N/A"
        deps = {}
        if version != self.__PendingPromotionCaption:
            if version in self.__promotedVersionsInfo:
                date = self.__promotedVersionsInfo[version]["date"]
                if 'directDependencies' in self.__promotedVersionsInfo[version]:
                    deps = self.__promotedVersionsInfo[version]["directDependencies"]
            
        if len(tickets) == 0:
            return ""

        return self.__Writer.printVersionBlock(version, deps, date, tickets)

    def copyWwwResources(self):
        # copy all images & web.config
        directory = pathToStoreReleaseNotes + '\\' + "images"
        if not os.path.exists(directory):
            os.makedirs(directory)

        wwwPath = os.path.dirname(os.path.realpath(__file__)) + '\\' + "www"   
        for filename in glob.glob(os.path.join(wwwPath + "\\images", '*.*')):
            shutil.copy(filename, pathToStoreReleaseNotes + "\\images")

        shutil.copy(wwwPath + '\\' + "web.config", pathToStoreReleaseNotes)
    
    def generateReleaseNotesByPromotedVersions(self):        
        
        self.__git.checkout()
        self.__git.retrieveHistory()
        self.__git.retrieveVersionsByGitHash( list(self.__promotedVersionsInfo.keys()) )
        self.__computeTicketsByVersion()
        
        lastPromotedVersion = self.__PendingPromotionCaption
        ticketsSoFar = []
        content = ""     

        hashesInVersion = self.__git.gitHistoryByVersion

        hashAlreadySeen = []
        noPromotedVersionSoFar = True
        sortedVersions = [] + hashesInVersion.keys();
        sortedVersions.sort(key=lambda s: map(int, s.split('.')))
        
        content = []
        # generate version blocks
        for version in sortedVersions:
        
            if version in self.__promotedVersionsInfo:
                print "Generating info for version " + version
                
            for hash in hashesInVersion[version]:
                if hash in hashAlreadySeen:
                    continue
                hashAlreadySeen = hashAlreadySeen + [hash]
                if hash in self.__git.gitCommitMessagesByHash:
                    ticketsSoFar = ticketsSoFar + self.__ticketProvider.extractTicketsFromMessage(self.__git.gitCommitMessagesByHash[hash])
                else:
                    print "Missing commit message info for "  + hash

            if version in self.__promotedVersionsInfo:
                content = content + [self.__printVersionBlock(version, ticketsSoFar)]           
                ticketsSoFar = []                

        if len(ticketsSoFar) > 0:
            content = content + [self.__printVersionBlock(self.__PendingPromotionCaption, ticketsSoFar)]           
        
        content.sort(reverse=True)        
        return "\n".join(content)
