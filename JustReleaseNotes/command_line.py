import json
import os
import argparse

import requests

import artifacters
import writers
import issuers
import sourcers
from sourcers import factory
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
            if "Releases" in conf:
                releasesConf = conf["Releases"]
                promotedVersionsInfo = artifacters.factory.create(releasesConf).retrievePromotedVersions()
            else:
                print ("No artifacter configured: every version tag will be considered a valid release")
                promotedVersionsInfo = {}

            issuesConf = conf["Issues"]
            ticketProvider = issuers.factory.create(issuesConf)

            directory = os.path.join(releaseNotesConfig["pathToSave"],packageName)
            conf["Source"]["Directory"] = directory
            repo = sourcers.factory.create(conf["Source"])
            writer = writers.factory.create(conf["ReleaseNotesWriter"], ticketProvider)

            generator = ReleaseNotes(conf, ticketProvider, writer, repo, promotedVersionsInfo)
            releaseNotes = generator.generateReleaseNotesByPromotedVersions()


            if not os.path.exists(directory):
                os.makedirs(directory)

            fileName = "index{0}".format(writer.getExtension())
            print ("\nStoring {0} release notes at {1}".format(packageName, os.path.join(directory,fileName)))
            f = open(os.path.join(directory,fileName), "wb")
            f.write(releaseNotes.encode('utf-8'))
            f.close()

if __name__ == '__main__':
    main()
