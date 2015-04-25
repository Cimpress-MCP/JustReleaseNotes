import importlib

def create(name, ticketProvider):
    try:
        module = importlib.import_module("JustReleaseNotes.writers.{0}".format(name))
        writerClass = getattr(module, name)
        return writerClass(ticketProvider)
    except:
        raise Exception("Release notes writer is needed to generate output: {0} not found".format(name))
