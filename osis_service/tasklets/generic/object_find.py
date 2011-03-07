__tags__ = 'osis', 'findobject',

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
        connection = OsisDB().getConnection('main')
        params['result'] = connection.objectsFind(params['domain'], 
                                     params['rootobjecttype'],
                                     params['filterobject'],
                                     params['osisview'])
