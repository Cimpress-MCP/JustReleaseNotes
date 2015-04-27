import importlib

def create(name):
   # try:
        module = importlib.import_module("JustReleaseNotes.artifacters.versioners.{0}".format(name))
        versionerClass = getattr(module, name)
        return versionerClass()
   # except:
   #     raise Exception("Version provider is needed to retrieve deployed versions: {0} was not found".format(name))
