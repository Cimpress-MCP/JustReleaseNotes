import importlib

def create(name, conf):
    try:
        module = importlib.import_module("JustReleaseNotes.issuers.{0}".format(name))
        issuerClass = getattr(module, name)
        return issuerClass(conf)
    except:
        raise Exception("Ticket provider is needed to retrieve ticket information: {0} not found".format(name))
