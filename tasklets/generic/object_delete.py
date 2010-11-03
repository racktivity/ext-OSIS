__tags__ = 'osis', 'delete'

from osis.store.OsisDB import OsisDB
def main(q, i, params, tags):
    con = OsisDB().getConnection('main')
    params['result'] = con.objectDelete(params['rootobjecttype'], params['rootobjectguid'], params['rootobjectversionguid'])