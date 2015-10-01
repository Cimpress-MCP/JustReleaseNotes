import json
import os
import os.path
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
    parser.add_argument('command', metavar='cmd', action="store", choices=['notes'])
    parser.add_argument('--config', '-c', '--c', metavar='config.json', nargs='?', help='Specifies the configuration to use', default="config.json")
    args = parser.parse_args()

    if args.command == "notes":
        generate_release_notes(args.config)

def generateForOneWriter(generator, ticketProvider, writerType, directory, fileName):
    print("\nGenerating using {0}".format(writerType))

    writer = JustReleaseNotes.writers.factory.create(writerType, ticketProvider)

    if fileName is None:
        fileName = "index{0}".format(writer.getExtension())

    content = ""
    p = os.path.join(directory, fileName)
    if os.path.isfile(p):
        f = open(p, "r")
        content = f.read()
        f.close()

    writer.setInitialContent(content)
    releaseNotes = generator.generateReleaseNotesByPromotedVersions(writer)

    print("\nStoring release notes at {0}".format(os.path.join(directory, fileName)))
    f = open(os.path.join(directory, fileName), "wb")
    f.write(releaseNotes.encode('utf-8'))
    f.close()

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

            if "Directory" in conf["Source"]:
                if not os.path.isabs(conf["Source"]["Directory"]):
                    conf["Source"]["Directory"] = os.path.join(currentDir, conf["Source"]["Directory"])
            else:
                conf["Source"]["Directory"] = directory

            repo = JustReleaseNotes.sourcers.factory.create(conf["Source"])

            if not os.path.exists(conf["Source"]["Directory"]):
                os.makedirs(conf["Source"]["Directory"])

            generator = ReleaseNotes(conf, ticketProvider, repo, promotedVersionsInfo)
            writerConfigs = conf["ReleaseNotesWriter"]
            if isinstance(writerConfigs, str):
                generateForOneWriter(generator, ticketProvider, writerConfigs, directory, None)
            elif hasattr(writerConfigs, '__iter__'):
                for writerConf in writerConfigs:
                    path = writerConf["PathToSave"]
                    generateForOneWriter(generator, ticketProvider, writerConf["Provider"], os.path.dirname(path), os.path.basename(path))

if __name__ == '__main__':
    main()
