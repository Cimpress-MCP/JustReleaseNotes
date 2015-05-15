import sys
import requests
import json
import io

class GitHubReleases:
    __defaultVersionRegex = "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+"
    __conf = []
    __promotedVersions = {}
        
    def __init__(self, conf):
        self.__promotedVersions = {}
        self.__conf = conf

    def __log(self, message):
        log = "GitHub Releases: " + message
        print(log)
        sys.stdout.flush()

    def retrievePromotedVersions(self):
        self.__log("Retrieving promoted from {0} at {1} ...".format(
            self.__conf["Provider"],
            self.__conf["Url"]))

        headers = { 'Authorization': self.__conf["Authorization"] }
        r = requests.get( self.__conf["Url"], headers = headers, verify=False )

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
