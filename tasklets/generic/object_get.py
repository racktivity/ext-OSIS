import osis
from osis.store.OsisDB import OsisDB
from osis.model.serializers import ThriftSerializer

__tags__ = 'osis', 'get'

def main(q, i, params, tags):
    q.logger.log('Getting %s'%(repr(params)), 5)
    osiscon = OsisDB().getConnection('main')
    serialized_rootobject = osiscon.objectGet(params['rootobjecttype'], params['rootobjectguid'], params['rootobjectversionguid'])
    rootobject_type = osis.ROOTOBJECT_TYPES[params['rootobjecttype']]
    rootobject = rootobject_type.deserialize(ThriftSerializer,serialized_rootobject)
    params['rootobject'] = rootobject