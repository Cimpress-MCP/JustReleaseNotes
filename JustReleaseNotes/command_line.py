import json
import os
import argparse

import requests

import JustReleaseNotes.artifacters
import JustReleaseNotes.writers
import JustReleaseNotes.issuers
import JustReleaseNotes.sourcers
from JustReleaseNotes.sourcers import factory
from JustReleaseNotes.issuers import factory
from JustReleaseNotes.writers import factory
from JustReleaseNotes.artifacters import factory
from JustReleaseNotes.releaseNotes import *
from JustReleaseNotes.utils import EnvReplacer

def main():
    parser = argparse.ArgumentParser(prog="just_release", description='Instruments release process.')
    parser.add_argument('command', metavar='cmd', action="store", choices=['notes'], default="notes")
    parser.add_argument('--config', '-c', '--c', metavar='config.json', nargs='?', help='Specifies the configuration to use', default="config.json")
    args = parser.parse_args()

    if args.command == "notes":
        generate_release_notes(args.config)

def generate_release_notes(configFile):
        requests.packages.urllib3.disable_warnings()
        file = open(configFile, 'r')
        fileContents = file.read()
        releaseNotesConfig = EnvReplacer.replace(json.loads(fileContents))
        currentDir = os.getcwd()
        if not os.path.isabs(releaseNotesConfig["pathToSave"]):
            releaseNotesConfig["pathToSave"] = os.path.join(currentDir, releaseNotesConfig["pathToSave"])

        for packageName, conf in releaseNotesConfig["packages"].items():
            if "Releases" in conf:
                releasesConf = conf["Releases"]
                promotedVersionsInfo = JustReleaseNotes.artifacters.factory.create(releasesConf).retrievePromotedVersions()
            else:
                print ("No artifacter configured: every version tag will be considered a valid release")
                promotedVersionsInfo = {}

            issuesConf = conf["Issues"]
            ticketProvider = JustReleaseNotes.issuers.factory.create(issuesConf)

            directory = os.path.join(releaseNotesConfig["pathToSave"],packageName)
            conf["Source"]["Directory"] = directory
            repo = JustReleaseNotes.sourcers.factory.create(conf["Source"])
            writer = JustReleaseNotes.writers.factory.create(conf["ReleaseNotesWriter"], ticketProvider)

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
