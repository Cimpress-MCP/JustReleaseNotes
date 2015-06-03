import JustReleaseNotes
from JustReleaseNotes import factory

def create(name, ticketProvider):
    return JustReleaseNotes.factory.createWithConfig("JustReleaseNotes.writers", name, ticketProvider)
