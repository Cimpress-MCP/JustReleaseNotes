import os, sys, re, subprocess
import requests
import json
import getpass
import glob
import shutil

from jira import *
from artifactory import *
from gitrepo import *
from releaseNotes import *    

# The Jira's SSL certificate is invalid and disabling ssl verification shows an annoying warning
requests.packages.urllib3.disable_warnings()

from releaseNotesConfiguration import releaseNotesConfig

# generate release notes
for packageName, conf in releaseNotesConfig["packages"].items():

    # automatically include some info... FIX ME, PLEASE!
    conf["PackageName"] = packageName
    conf["JiraConf"] = releaseNotesConfig["JiraConf"]
    conf["WebImagesPath"] = releaseNotesConfig["WebImagesPath"]
    conf["StorageUrl"] = releaseNotesConfig["Artifactory"]["StorageUrl"]
    
    if 'DirectDependencies' in conf:
        conf["DirectDependenciesInfo"] = {}
        for dep in list(conf["DirectDependencies"].keys()):
            if dep in releaseNotesConfig["packages"]:
                conf["DirectDependenciesInfo"][dep] = releaseNotesConfig["packages"][dep]
        
    artifactory = Artifactory(conf)
    promotedVersionsInfo = artifactory.retrievePromotedVersions()
    
    gitRepo = GitRepo(conf)
    generator = ReleaseNotes(conf, gitRepo, promotedVersionsInfo)
    releaseNotes = generator.generateReleaseNotesByPromotedVersions()
    
    directory = releaseNotesConfig["pathToSave"] + '\\' + packageName
    if not os.path.exists(directory):
        os.makedirs(directory)
            
    print ("\nStoring {0} release notes at {1}\n".format(packageName, directory + '\\index.html'))
    f = open( directory + '\\index.html', "wb")
    f.write(releaseNotes.encode('utf-8'))
    f.close()
        