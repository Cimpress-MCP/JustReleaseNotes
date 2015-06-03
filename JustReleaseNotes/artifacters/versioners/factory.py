import JustReleaseNotes
from JustReleaseNotes import factory

def create(name):
    return JustReleaseNotes.factory.createWithName("JustReleaseNotes.artifacters.versioners", name)