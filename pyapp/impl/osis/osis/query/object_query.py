
def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname) 
    params['result'] = osis.runQuery(params['query'], *params['args'], **params['kwargs'])
