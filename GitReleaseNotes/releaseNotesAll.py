import artifacters
import writers
import issuers
import requests
import json
from artifacters import factory
from writers import factory
from issuers import factory
from releaseNotes import *

requests.packages.urllib3.disable_warnings()

if (len(sys.argv) < 2):
    print "Provide configuration file with json as parameter."
    sys.exit(1)

file = open(sys.argv[1], 'r')
fileContents = file.read()
releaseNotesConfig = json.loads(fileContents)

for packageName, conf in releaseNotesConfig["packages"].items():

    releasesConf = conf["Releases"]
    promotedVersionsInfo = artifacters.factory.create(releasesConf["Provider"], releasesConf).retrievePromotedVersions()
    issuesConf = conf["Issues"]
    ticketProvider = issuers.factory.create(issuesConf["Provider"], issuesConf)

    conf["PackageName"] = packageName
    gitRepo = GitRepo(conf)
    writer = writers.factory.create(conf["ReleaseNotesWriter"], ticketProvider)

    generator = ReleaseNotes(conf, ticketProvider, writer, gitRepo, promotedVersionsInfo)
    releaseNotes = generator.generateReleaseNotesByPromotedVersions()
    
    directory = releaseNotesConfig["pathToSave"] + '\\' + packageName
    if not os.path.exists(directory):
        os.makedirs(directory)

    fileName = "index{0}".format(writer.getExtension())
    print ("\nStoring {0} release notes at {1}\n".format(packageName, directory + '\\' + fileName))
    f = open( directory + '\\' + fileName, "wb")
    f.write(releaseNotes.encode('utf-8'))
    f.close()
