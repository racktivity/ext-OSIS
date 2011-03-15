__tags__ = 'osis', 'delete'
__priority__= 1 # Lowest priority 

from osis.store.OsisDB import OsisDB
def main(q, i, params, tags):
    key  = 'osis.%s.%s.%s'  % (params['domain'], params['rootobjecttype'], params['rootobjectguid'])
    arakoonClient = q.clients.arakoon.getClient('cluster1')
    if arakoonClient.exists(key): 
        arakoonClient.delete(key)
