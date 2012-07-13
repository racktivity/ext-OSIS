import time

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    root = params['rootobject']
    domain = params['domain']
    osis.objectSave(domain, root)
