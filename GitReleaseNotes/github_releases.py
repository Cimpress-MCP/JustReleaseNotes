import os, sys, re, subprocess
import requests
import json
import getpass
import tempfile
from filever import *
import xml.etree.ElementTree as ET

class GitHubReleases:
    __defaultVersionRegex = "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+"
    __conf = []
    __promotedVersions = {}
        
    def __init__(self, conf):
        self.__promotedVersions = {}
        self.__conf = conf

    def __log(self, message):
        print ("GitHub Releases: " + message)
        sys.stdout.flush()

    def retrievePromotedVersions(self):
        self.__log("Retrieving promoted from ({0}) at {1} ...".format(
            self.__conf["Provider"],
            self.__conf["Url"]))

        r = requests.get( self.__conf["Url"] )
        response = json.loads(r.text)
        
        for release in response:
            version = release["name"]
            self.__promotedVersions[version] = {
                "date" : release["published_at"],
                }
        
        if len(self.__promotedVersions) == 0:
            raise ValueError("Failed to retrieve promoted version. Please check if configuration is correct")
        
        self.__log("Found {0} promoted versions".format(len(self.__promotedVersions)))
        return self.__promotedVersions
