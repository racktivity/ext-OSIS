__tags__ = 'osis', 'query'

from osis.store.OsisDB import OsisDB
def main(q, i, params, tags):
    con = OsisDB().getConnection('main')
    params['result'] = con.runQuery(params['query'])