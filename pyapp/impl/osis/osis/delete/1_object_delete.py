
def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    params['result'] = osis.objectDelete(params['domain'], params['rootobjecttype'], params['rootobjectguid'])
