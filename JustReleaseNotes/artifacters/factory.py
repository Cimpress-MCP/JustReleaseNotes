import JustReleaseNotes
from JustReleaseNotes import factory

def create(conf):
    return JustReleaseNotes.factory.createWithConfig("JustReleaseNotes.artifacters", conf["Provider"], conf)