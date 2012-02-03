
def main(q, i, p, params, tags):
    key  = 'osis.%s.%s.%s'  % (params['domain'], params['rootobjecttype'], params['rootobjectguid'])
    arakoonClient = q.clients.arakoon.getClient(p.api.appname)
    if arakoonClient.exists(key): 
        arakoonClient.delete(key)
