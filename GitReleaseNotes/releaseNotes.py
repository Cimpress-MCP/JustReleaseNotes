import os, sys, re, subprocess
import requests
import json
import getpass

from jira import *
from gitrepo import *

class ReleaseNotes:

    __PendingPromotionCaption = "Pending promotion"
    __Format = "jira"
    __conf = {}
    __ticketsByVersion = {}
    __promotedVersionsInfo = {}
    __ticketReplacements = {}
    
    def __init__(self, conf, git, promotedVersionsInfo):
        self.__ticketsByVersion = {}
        self.__conf = conf
        if "PendingPromotionCaption" in conf:
            self.__PendingPromotionCaption = conf["PendingPromotionCaption"]
        if "ReleaseNotesFormat" in conf:
            self.__Format = conf["ReleaseNotesFormat"]
        self.__git = git
        self.__promotedVersionsInfo = promotedVersionsInfo
        
        self.__ticketReplacements = {}
        if "TicketReplacements" in conf:
            self.__ticketReplacements = conf["TicketReplacements"]    

    def __extractTicketsFromMessage(self, message):        
        if message.find("#noissue") != -1:
            return ["FD-00000"]
        message = message.replace("\n", " ").replace("\r", " ").replace("\t", " ");
        p = re.compile('FD-[0-9]+');
        return p.findall(message)
        
    def __computeTicketsByVersion(self):
        currentVersion = "latest"        
        self.__ticketsByVersion[currentVersion] = []
        for hash in self.__git.gitCommitsList:
            if hash in self.__git.versionsByGitHash:
                currentVersion = self.__git.versionsByGitHash[hash] 
                self.__ticketsByVersion[currentVersion] = []
            tickets = self.__extractTicketsFromMessage(self.__git.gitCommitMessagesByHash[hash])
            self.__ticketsByVersion[currentVersion] = self.__ticketsByVersion[currentVersion] + tickets     
     
    def __printVersionBlock(self, version, tickets):        
        date = "N/A"
        deps = {}
        if version != self.__PendingPromotionCaption:
            if version in self.__promotedVersionsInfo:
                date = self.__promotedVersionsInfo[version]["date"]
                deps = self.__promotedVersionsInfo[version]["directDependencies"]
            
        if len(tickets) == 0:
            return ""
            
        if self.__Format == "jira":
            return self.__printJiraFormattedVersionBlock(version, deps, date, tickets)

        if self.__Format == "html":
            return self.__printHtmlFormattedVersionBlock(version, deps, date, tickets)
            
        raise ValueError("Ops, unsupported format :)")
        
    def __printJiraFormattedVersionBlock(self, version, deps, date, tickets):
        lines = [
            "<div class=\"mw-collapsible\" style=\"width:100%; border: 0px\">",
            "<big>'''" + version + "'''" + " (Date: " + date + ")</big>",
            "<div class=\"mw-collapsible-content\">",
            ]
            
        uniqTickets = sorted( set(tickets), reverse=True)
        for ticket in uniqTickets:
            if ticket == "FD-00000":
                lines.append("* Stability improvements")
            else:
                lines.append("* {{JiraTrain with summary |" + ticket + "}}")
                
        return '\n'.join(lines + [ "</div>", "</div>", "<hr>" ])
        
    def __printHtmlFormattedVersionBlock(self, version, deps, date, tickets):
        data = [
            "<div style=\"width:100%; border: 0px\">",
            "<a name=\"" + version + "\"></a>",
            "<h2>" + version + "<sup><small style=\"font-size:10px\"><i> " + date + "</i></small></sup></h2>",
            ]
        
        d = []
        for item in list(deps.keys()): 
            if item in self.__conf["DirectDependenciesInfo"]:
                d.append( '<a href="{2}#{1}">{0} {1}</a>'.format(
                    item, deps[item], 
                    self.__conf["DirectDependenciesInfo"][item]["WikiPageTitle"]))
            else:
                if item == "ANY":
                    d.append(deps[item])
                else:
                    d.append( '{0} {1}'.format(item, deps[item]))
                
        if len(d) > 0:
            data.append('<div style="background: #eee; "><i>Components: ')
            data.append('; '.join(d))
            data.append('</i></div>')
            
        data.append("<ul>")
        uniqTickets = sorted(set(tickets), reverse=True)
        
        # Make sure we don't have unwanted tickets (yes, this happens...)
        for candidate in list(self.__ticketReplacements.keys()):
            if candidate in uniqTickets:
                uniqTickets.remove(candidate)
                uniqTickets = uniqTickets + [self.__ticketReplacements[candidate]]
                
        uniqTickets = sorted(set(uniqTickets), reverse=True)
                
        for ticket in uniqTickets:        
            if ticket == "FD-00000":
                data.append("<li style=\"font-size:14px\">Stability improvements</li>")
            else:
                data.append("<li style=\"font-size:14px\">" + self.__printJiraTicketInfo(ticket) + "</li>")
        
        data = data + ["</ul>", "</div>", ""]
        
        return '\n'.join(data)    
    
    def __fieldIcon(self, f):
        parts = f["iconUrl"].split("/")
        return '<img src="{0}{1}" alt="{1}" title="{2}"/>'.format(self.__conf["WebImagesPath"], parts[len(parts)-1], f["name"])
    
    def __printJiraTicketInfo(self, ticket):
        jira = JiraReader(self.__conf["JiraConf"])
        data = jira.readJsonInfo(ticket)   

        r = [
            self.__fieldIcon(data["fields"]["issuetype"]),
            self.__fieldIcon(data["fields"]["status"]),
            self.__fieldIcon(data["fields"]["priority"]),
            '<a href="{0}{1}" class="extiw">{1}</a>'.format(self.__conf["JiraConf"]["JiraBrowseUrl"], ticket),
            data["fields"]["summary"],
            ]
        
        return ' '.join(r) + '\n'
        
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
        sortedVersionsInDescendingOrder = [] + hashesInVersion.keys();
        sortedVersionsInDescendingOrder.sort(key=lambda s: map(int, s.split('.')), reverse=True)
        
        # generate version blocks
        for version in sortedVersionsInDescendingOrder:
            if version in self.__promotedVersionsInfo and noPromotedVersionSoFar == True:
                noPromotedVersionSoFar = False
                content = content + self.__printVersionBlock(self.__PendingPromotionCaption, ticketsSoFar)           
                ticketsSoFar = []                
             
            if version in self.__promotedVersionsInfo:
                print "Generating info for version " + version
                
            for hash in hashesInVersion[version]:
                if hash in hashAlreadySeen:
                    continue
                hashAlreadySeen = hashAlreadySeen + [hash]
                if hash in self.__git.gitCommitMessagesByHash:
                    ticketsSoFar = ticketsSoFar + self.__extractTicketsFromMessage(self.__git.gitCommitMessagesByHash[hash])
                else:
                    print "Missing commit message info for "  + hash

            if version in self.__promotedVersionsInfo:
                content = content + self.__printVersionBlock(version, ticketsSoFar)           
                ticketsSoFar = []                

        return content
