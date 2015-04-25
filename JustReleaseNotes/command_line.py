import requests
import json
import os
import artifacters
import writers
import issuers
import argparse
from gitrepo import GitRepo
from issuers import factory
from writers import factory
from artifacters import factory
from releaseNotes import *

def main():
    parser = argparse.ArgumentParser(prog="just_release", description='Instruments release process.')
    parser.add_argument('command', metavar='N', action="store", choices=['notes'])
    parser.add_argument('--config', '-c', '--c', metavar='config.json', nargs='?', help='Specifies the configuration to use')
    args = parser.parse_args()

    if args.command == "notes":
        requests.packages.urllib3.disable_warnings()
        if args.config != None:
            file = open(args.config, 'r')
        else:
            file = open("config.json", 'r')
        fileContents = file.read()
        releaseNotesConfig = json.loads(fileContents)
        currentDir = os.getcwd()
        if not os.path.isabs(releaseNotesConfig["pathToSave"]):
            releaseNotesConfig["pathToSave"] = os.path.join(currentDir, releaseNotesConfig["pathToSave"])

        for packageName, conf in releaseNotesConfig["packages"].items():
            releasesConf = conf["Releases"]
            promotedVersionsInfo = artifacters.factory.create(releasesConf["Provider"], releasesConf).retrievePromotedVersions()
            issuesConf = conf["Issues"]
            ticketProvider = issuers.factory.create(issuesConf["Provider"], issuesConf)

            conf["PackageName"] = packageName
            conf["pathToSave"] = releaseNotesConfig["pathToSave"]
            gitRepo = GitRepo(conf)
            writer = writers.factory.create(conf["ReleaseNotesWriter"], ticketProvider)

            generator = ReleaseNotes(conf, ticketProvider, writer, gitRepo, promotedVersionsInfo)
            releaseNotes = generator.generateReleaseNotesByPromotedVersions()

            directory = os.path.join(releaseNotesConfig["pathToSave"],packageName)
            if not os.path.exists(directory):
                os.makedirs(directory)

            fileName = "index{0}".format(writer.getExtension())
            print ("\nStoring {0} release notes at {1}\n".format(packageName, os.path.join(directory,fileName)))
            f = open(os.path.join(directory,fileName), "wb")
            f.write(releaseNotes.encode('utf-8'))
            f.close()

if __name__ == '__main__':
    main()
