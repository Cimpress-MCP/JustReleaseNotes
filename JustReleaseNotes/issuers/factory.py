import JustReleaseNotes
from JustReleaseNotes import factory

def create(conf):
    if isinstance(conf, list):
        return JustReleaseNotes.issuers.AggregateIssuer.AggregateIssuer(conf)
    else:
        return JustReleaseNotes.factory.createWithConfig("JustReleaseNotes.issuers", conf["Provider"], conf)
