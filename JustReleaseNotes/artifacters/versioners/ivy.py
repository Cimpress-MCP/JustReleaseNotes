import xml.etree.ElementTree as ET

class ivy:

    def extractVersions(self, fileName):
        tree = ET.parse(fileName)
        root = tree.getroot()
        deps = root.findall('./dependencies/dependency')
        res = []
        for dep in deps:
            v = dep.attrib['name'] + ": " + dep.attrib['rev']
            if 'revConstraint' in dep.attrib:
                v = v + " (" + dep.attrib['revConstraint'] + ")"
            res.append(v)
        return res