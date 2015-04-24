import importlib
import GitHubReleases

def create(name, conf):
    try:
        module = importlib.import_module("artifacters.{0}".format(name))
        artifacterClass = getattr(module, name)
        return artifacterClass(conf)
    except:
        raise Exception("Artifacts provider is needed to retrieve deployed versions: {0} was not found".format(name))
