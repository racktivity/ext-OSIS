import osis
from osis.store.OsisDB import OsisDB
from pymodel.serializers import ThriftSerializer

__tags__ = 'osis', 'get'

def main(q, i, params, tags):
    from pymodel import ROOTOBJECT_TYPES
    q.logger.log('Getting %s'%(repr(params)), 5)
    osiscon = OsisDB().getConnection('main')
    serialized_rootobject = osiscon.objectGet(params['domain'], params['rootobjecttype'], params['rootobjectguid'], params['rootobjectversionguid'])
    rootobject_type = ROOTOBJECT_TYPES[params['domain']][params['rootobjecttype']]
    rootobject = rootobject_type.deserialize(ThriftSerializer, serialized_rootobject)
    params['rootobject'] = rootobject
