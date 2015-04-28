import importlib

def create(conf):
    #try:
        module = importlib.import_module("JustReleaseNotes.sourcers.{0}".format(conf["Provider"]))
        issuerClass = getattr(module, conf["Provider"])
        return issuerClass(conf)
    #except:
    #    raise Exception("Source code repository is needed to retrieve tags: {0} not found".format(conf["Provider"]))
