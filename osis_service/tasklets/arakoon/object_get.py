__tags__ = 'osis', 'get'
__priority__= 1 # Lowest priority 

from osis.store.OsisDB import OsisDB
def main(q, i, params, tags):
    domain = params['domain']
    type_ = params['rootobjecttype']
    key  = 'osis.%s.%s.%s'  % (domain, type_, params['rootobjectguid'])
    arakoonClient = q.clients.arakoon.getClient('cluster1')
    root = arakoonClient.get(key)
    from pymodel.serializers import ThriftSerializer
    from pymodel import ROOTOBJECT_TYPES
    return ThriftSerializer.deserialize(ROOTOBJECT_TYPES[domain][type_], root)
