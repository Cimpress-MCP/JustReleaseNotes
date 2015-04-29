import re
import os

def replace(config):
    if type(config) is dict:
        return __replaceDict(config)
    elif type(config) is list:
        return __replaceList(config)
    elif type(config) is str:
        return __replaceStr(config)
    else:
        return config


def __replaceDict(config):
    result = {}
    for key in config:
        result[key] = replace(config[key])
    return result


def __replaceList(config):
    return [replace(x) for x in config]


def __replaceStr(strValue):
    if type(strValue) is str:
        matches = re.findall('ENV\[([0-9a-zA-Z_]+)\]', strValue, re.IGNORECASE)
        if matches is None or len(matches) == 0:
            return strValue
        else:
            r = strValue
            for i in matches:
                insensitive_env = re.compile(re.escape("ENV[{0}]".format(i)), re.IGNORECASE)
                r = insensitive_env.sub(os.environ[i], r)
            return r
    else:
        return strValue