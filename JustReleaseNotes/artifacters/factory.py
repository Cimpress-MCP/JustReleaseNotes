import importlib

def create(conf):
    try:
        module = importlib.import_module("JustReleaseNotes.artifacters.{0}".format(conf["Provider"]))
        artifacterClass = getattr(module, conf["Provider"])
        return artifacterClass(conf)
    except:
        raise Exception("Artifacts provider is needed to retrieve deployed versions: {0} was not found".format(conf["Provider"]))
