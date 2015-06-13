import importlib
import sys

def createWithConfig(module, name, conf):
    try:
        module = importlib.import_module(module + ".{0}".format(name))
        clazz = getattr(module, name)
        return clazz(conf)
    except:
        e = sys.exc_info()[1]
        raise Exception("Unable to create module provider {0} from module {1}: {2}".format(conf["Provider"], module, e))

def createWithName(module, name):
   try:
        module = importlib.import_module(module + ".{0}".format(name))
        clazz = getattr(module, name)
        return clazz()
   except:
        e = sys.exc_info()[1]
        raise Exception("Unable to create module provider {0} from module {1}: {2}".format(name, module, e))