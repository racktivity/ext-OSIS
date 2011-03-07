__tags__ = 'osis', 'findasview',

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
        connection = OsisDB().getConnection('main')
        params['result'] = connection.objectsFindAsView(params['domain'],
                                     params['rootobjecttype'],
                                     params['filterobject'],
                                     params['osisview'])
