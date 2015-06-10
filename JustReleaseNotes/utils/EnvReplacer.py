import re
import os

def replace(config):
    if type(config) is dict:
        return __replaceDict(config)
    elif type(config) is list:
        return __replaceList(config)
    elif type(config) is int:
        return config
    elif type(config) is float:
        return config
    else:
        return __replaceStr(str(config))

def __replaceDict(config):
    result = {}
    for key in config:
        result[key] = replace(config[key])
    return result


def __replaceList(config):
    return [replace(x) for x in config]


def __replaceStr(str):
    return re.sub(r'ENV\[(\w+)\]', __findEnvKey, str, flags=re.IGNORECASE)


def __findEnvKey(match):
    return os.environ[match.group(1)]