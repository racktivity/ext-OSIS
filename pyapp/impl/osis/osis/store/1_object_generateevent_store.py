
def main(q, i, p, params, tags):
    root = params['rootobject']
    type = params['rootobjecttype']
    domain = params['domain'] 
    p.api.events.publish('pylabs.event.%s.osis.store.%s.%s' % (p.api.appname, domain, type), root.guid)
