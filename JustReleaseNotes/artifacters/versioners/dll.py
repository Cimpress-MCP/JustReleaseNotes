import os

from JustReleaseNotes.artifacters.versioners.filever import calcversioninfo


class dll:

    def extractVersions(self, fileName):
        if fileName is None:
            return None
        dependencyVersion = calcversioninfo(fileName)
        os.remove(fileName)
        res = []
        res.append("{0}: {1}".format(os.path.basename(fileName), dependencyVersion))
        return res