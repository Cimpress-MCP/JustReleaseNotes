import os, sys, re, subprocess
from git import Repo
        
class GitRepo:
    __repo = ""
    __repoX = ""
    __packageName = ""
    
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
        self.__repo = conf["GitRepositoryUrl"] 
        self.__packageName = conf["PackageName"]
        self.__repoX = ""
        self.pathToSave = conf["pathToSave"]
        
    def __log(self, message):
        print ("Git: " + message)
        sys.stdout.flush()
        
    def checkout(self):
        path = self.pathToSave + "\\" + self.__packageName
        if not os.path.isdir(path):
            self.__log("Creating folder at: " + path)
            os.makedirs(path)

        os.chdir(path)
        self.__log("Cloning " + self.__repo + " at " + path)
        subprocess.Popen("git clone " + self.__repo + " ." ).wait()
        subprocess.Popen("git pull").wait()
        self.__repoX = Repo(".")

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
    
    def retrieveHistory(self):
        self.__log("Retrieving Git history...")        
        for i in self.__repoX.iter_commits('master', max_count=1024):
            self.gitCommitMessagesByHash[i.hexsha] = i.summary + i.message
            self.gitCommitsList.append(i.hexsha)
            self.gitDatesByHash[i.hexsha] = i.authored_date  
            self.setParents(i)
        
    def __optimizeHistoryByVersion(self):        
        sortedVersionsInAscendingOrder = [] + self.gitHistoryByVersion.keys()
        sortedVersionsInAscendingOrder.sort(key=lambda s: map(int, s.split('.')), reverse=False)
        
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
            raise ValueError("Make sure you first retrieve the promoted version")
        
        tags = self.__repoX.tags
        for t in tags:
            tag = "" + str(t)
            hexsha = str(t.commit)
            if tag.startswith("non-published"):
                continue

            version = tag.split("/")[-1]
            if not re.match("^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$", version):
                continue

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
            
        self.__optimizeHistoryByVersion()