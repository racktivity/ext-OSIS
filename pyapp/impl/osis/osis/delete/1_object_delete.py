
def main(q, i, p, params, tags):
    key  = 'osis.%s.%s.%s'  % (params['domain'], params['rootobjecttype'], params['rootobjectguid'])
    if p.api.db.exists(key): 
        p.api.db.delete(key)
