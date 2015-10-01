import os, sys, re
from git import Repo
        
class GitRepo:
    __repo = ""
    __repoX = ""
    __packageName = ""
    __remote = "origin"
    __branch = "master"
    
    gitCommitsList = []
    gitCommitMessagesByHash = {}
    gitDatesByHash = {}
    versionsByGitHash = {}
    commitParents = {}
    gitHistoryByVersion = {}
    
    def __init__(self, conf):
        self.gitCommitsList = []
        self.gitCommitMessagesByHash = {}
        self.gitDatesByHash = {}
        self.versionsByGitHash = {}
        self.gitHistoryByVersion = {}
        self.__repo = conf["RepositoryUrl"]
        self.__directory = conf["Directory"]
        self.__repoX = ""
        self.__versionTagRegex = "^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$"

        if "VersionTagRegex" in conf:
            self.__versionTagRegex = conf["VersionTagRegex"]

        if "Remote" in conf:
            self.__remote = conf["Remote"]

        if "Branch" in conf:
            b = conf["Branch"]
            pos = b.find("/")
            if (pos >= 0):
                self.__remote = b[:pos]
                self.__branch = b[pos+1:]
            else:
                self.__branch = b


        
    def __log(self, message):
        print ("Git: " + message)
        sys.stdout.flush()
        
    def checkout(self):
        path = self.__directory
        if not os.path.isdir(path):
            self.__log("Creating folder at: " + path)
            os.makedirs(path)

        self.__log("Cloning " + self.__repo + " at " + path)
        try:
            self.__repoX = Repo.clone_from(self.__repo, path)
            release_notes_head = self.__repoX.create_head(self.__branch, self.__remote + "/" + self.__branch)
            self.__repoX.head.reference = release_notes_head
            self.__repoX.head.reset(index=True, working_tree=True)
        except:
            self.__repoX = Repo(path)
            self.__repoX.head.reference = self.__repoX.heads[self.__branch]

    def setParents(self, commit):
        if len(commit.parents) == 0:
            return
            
        if commit.hexsha in self.commitParents:
            # Already traversed
            return

        self.commitParents[commit.hexsha] = []
        for p in commit.parents:
            self.commitParents[commit.hexsha] = self.commitParents[commit.hexsha] + [p.hexsha]
            self.setParents(p)
            
    def __getParentsListForVersion(self, hash, version, resultsSoFar):
        if hash in resultsSoFar:
            return []
        if hash not in self.commitParents:
            return []
        results = [hash]
        for p in self.commitParents[hash]:
            if p not in self.versionsByGitHash:
                results = results + self.__getParentsListForVersion(p, version, resultsSoFar + results)
        return results

    def processCommit(self, commitHash):
        self.__processCommit(self.__repoX.commit(commitHash))

    def __processCommit(self, commit):
        self.gitCommitMessagesByHash[commit.hexsha] = commit.summary + commit.message
        self.gitCommitsList.append(commit.hexsha)
        self.gitDatesByHash[commit.hexsha] = commit.authored_date
        self.setParents(commit)

    def retrieveHistory(self):
        self.__log("Retrieving Git history...")        
        for i in self.__repoX.iter_commits(self.__branch, max_count=1024):
            self.__processCommit(i)
        
    def __optimizeHistoryByVersion(self):        
        sortedVersionsInAscendingOrder = [] + list(self.gitHistoryByVersion.keys())
        sortedVersionsInAscendingOrder.sort(key=lambda s: list(map(int, s.split('.'))), reverse=False)
        
        # remove commits part of newer versions if they exists in older one        
        hashUsedForVersion = {}
        for version in sortedVersionsInAscendingOrder:
            for hash in self.gitHistoryByVersion[version]:
                if hash in hashUsedForVersion:
                    x = [] + self.gitHistoryByVersion[version]
                    x.remove(hash)
                    self.gitHistoryByVersion[version] = [] + x
                else:
                    hashUsedForVersion[hash] = version
        
    def retrieveVersionsByGitHash(self, promotedVersionsList):
        self.__log("Retrieving versions (git tags)...")

        if len(promotedVersionsList) == 0:
            print("Make sure you first retrieve the promoted version: Promoted versions are empty, thus every tag "
                  "matching will be considered as released")
        
        tags = self.__repoX.tags
        for t in tags:
            tag = "" + str(t)
            hexsha = str(t.commit)
            if tag.startswith("non-published"):
                continue

            version = tag.split("/")[-1]
            p = re.compile(self.__versionTagRegex)
            m = p.match(version)
            if not m:
                continue

            g = m.groups()
            if len(g)>1:
                continue;
            elif len(g) == 1:
                version = g[0];

            if hexsha in self.versionsByGitHash:
                v1 = version
                v2 = self.versionsByGitHash[hexsha]
                self.__log("Warning: Multiple versions for the same commit={0} v1={1} v2={2}".format(hexsha,v1,v2))
                self.versionsByGitHash[hexsha] = v1
                if v1 not in promotedVersionsList and v2 in promotedVersionsList:
                    self.versionsByGitHash[hexsha] = v2
                self.__log("Warning: Choosing {0} (promoted={1})".format(
                    self.versionsByGitHash[hexsha], 
                    self.versionsByGitHash[hexsha] in promotedVersionsList))
            else:
                self.versionsByGitHash[hexsha] = version     

            self.gitHistoryByVersion[version] = self.__getParentsListForVersion(hexsha,version, [])

        self.__addHeadIfNotPresent()
        self.__optimizeHistoryByVersion()

    def __addHeadIfNotPresent(self):
        hexsha = str(self.__repoX.heads[self.__branch].commit)
        if hexsha not in self.versionsByGitHash:
            version = str(sys.maxsize)
            self.versionsByGitHash[hexsha] = version
            self.gitHistoryByVersion[version] = self.__getParentsListForVersion(hexsha, version, [])