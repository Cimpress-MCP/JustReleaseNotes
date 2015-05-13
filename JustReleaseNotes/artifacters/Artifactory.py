import sys
import re
import json
import tempfile
import os
import JustReleaseNotes.artifacters.versioners
from JustReleaseNotes.artifacters.versioners import factory
import requests


class Artifactory:
    __artifactoryUrl = None
    __defaultVersionRegex = "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+"
    __conf = []
    __promotedVersions = {}
        
    def __init__(self, conf):
        self.__promotedVersions = {}
        self.__conf = conf
        self.__artifactoryUrl = self.__conf["StorageUrl"]

    def __log(self, message):
        print ("Artifactory: " + message)
        sys.stdout.flush()
        
    def __retrievePromotionDate(self, version):
        self.__log("Retrieving info for version {0}".format(version))
        uri = "{0}/{1}/{2}/{3}".format(
            self.__artifactoryUrl,
            self.__conf["Repository"],
            self.__conf["ArtifactUri"],
            version)
        r = requests.get( uri )
        response = json.loads(r.text)
        
        if "created" in response:
            return response["created"][:10]
        else:
            self.__log("No 'created' for version {0}".format(version))
            
        return "n/a"
        
    def __downloadFile(self, uri):
        r = requests.get( uri )
        if r.status_code == 404:
            return None
            
        response = json.loads(r.text)
        if not "downloadUri" in response:
            self.__log("Failed to get 'downloadUri' from response.")
            return None
            
        self.__log("Download URI: {0}".format(response["downloadUri"]))
        
        #        
        r = requests.get(response["downloadUri"], stream=True)
        if r.status_code != 200:
            return None

        b = bytes()
        for chunk in r.iter_content(1024):
            b += chunk
        return b

    def retrieveDependeciesVersions(self, version):
        if "DirectDependencies" not in self.__conf:
            return {}
    
        if len(self.__conf["DirectDependencies"].keys()) == 0:
            return {}
        
        result = {}
        for packageName in list(self.__conf["DirectDependencies"].keys()):
            
            dep = self.__conf["DirectDependencies"][packageName]

            versionsExtractor = JustReleaseNotes.artifacters.versioners.factory.create(dep["type"])
            if packageName == "ANY":
                if dep["type"] == "ivy":
                    uri = "{0}/{1}/{2}/ivy-{2}.xml".format(
                        self.__conf["Repository"],
                        self.__conf["ArtifactUri"],
                        version).replace("//","/")
                    fullUrl = "{0}/{1}".format(self.__artifactoryUrl,uri)
                    result[packageName] = '; '.join(versionsExtractor.extractVersions(self.__downloadFile(fullUrl), fullUrl))
                else:
                   raise ValueError( "Unsupported dependency type '{0}' for ANY".format(dep["type"]))
            else:
                # Extract from DLL
                if dep["type"] == "dll":
                    uri = "{0}/{1}/{2}/{3}".format(
                        self.__conf["Repository"],
                        self.__conf["ArtifactUri"],
                        version,
                        dep["name"]).replace("//","/")
                    fullUrl = "{0}/{1}".format(self.__artifactoryUrl,uri)
                    dependencyVersions = versionsExtractor.extractVersions(self.__downloadFile(fullUrl), fullUrl)
                    if dependencyVersions is None:
                        continue
                    result[packageName] = '; '.join(dependencyVersions)
                else:
                    raise ValueError( "Unsupported dependency type '{0}'".format(dep[packageName]["type"]))
        
        return result
          
    def __extractVersion(self, version):
        versionRegex = self.__defaultVersionRegex
        if "RegexToExtractVersion" in self.__conf:
            versionRegex = self.__conf["RegexToExtractVersion"]
        regex = re.compile(versionRegex)

        extractedVersion = regex.findall(version)      
        if len(extractedVersion) == 0:
            self.__log("Failed to find version in '{0}' using '{1}'".format(version, versionRegex))
            return None
        if len(extractedVersion) > 1:
            self.__log("Multiple versions are matching the regex for: '{0}'".format(version))
            return None
            
        return extractedVersion[0].replace("_",".")
    

    def retrievePromotedVersions(self):
        self.__log("Retrieving promoted ({0}) versions {1} ...".format(
            self.__conf["Repository"],
            self.__conf["ArtifactUri"]))

        uri = "{0}/{1}".format(self.__artifactoryUrl,self.__conf["Repository"]);
        artifactPath=self.__conf["ArtifactUri"];
        if (artifactPath[0] == "/"):
            uri += artifactPath
        else:
            uri += "/" + artifactPath
            
        r = requests.get( uri )
        response = json.loads(r.text)
        
        for child in response["children"]:
            version = child["uri"][1:]

            extractedVersion = self.__extractVersion(version)
            if extractedVersion is None:
                continue
            
            self.__promotedVersions[extractedVersion] = {
                "date" : self.__retrievePromotionDate(version),
                "directDependencies" : self.retrieveDependeciesVersions(version)
                }
        
        if len(self.__promotedVersions) == 0:
            raise ValueError("Failed to retrieve promoted version. Please check artifactory configuration is correct")
        
        self.__log("Found {0} promoted versions".format(len(self.__promotedVersions)))
        return self.__promotedVersions