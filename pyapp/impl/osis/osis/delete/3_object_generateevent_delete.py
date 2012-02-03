
def main(q, i, p, params, tags):
    guid = params['rootobjectguid']
    type = params['rootobjecttype']
    domain = params['domain'] 
    p.api.events.publish('pylabs.event.%s.osis.delete.%s.%s' % (p.api.appname, domain, type), guid)
