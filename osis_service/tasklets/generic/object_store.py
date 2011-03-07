__author__ = 'aserver'
__tags__ ='osis', 'store'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    osis = OsisDB().getConnection('main')
    root = params['rootobject']
    domain = params['domain']
    osis.objectSave(domain, root)
