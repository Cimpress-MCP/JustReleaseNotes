import re
import sys

class BaseWriter:

    def convertVersion(self, version):
        if (version == str(sys.maxsize)):
            version = "Upcoming developments"
        return version