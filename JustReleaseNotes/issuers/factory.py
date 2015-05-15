import importlib

def create(conf):
    try:
        module = importlib.import_module("JustReleaseNotes.issuers.{0}".format(conf["Provider"]))
        issuerClass = getattr(module, conf["Provider"])
        return issuerClass(conf)
    except:
        raise Exception("Ticket provider is needed to retrieve ticket information: {0} not found".format(conf["Provider"]))

