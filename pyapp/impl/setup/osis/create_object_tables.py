__author__ = 'Racktivity'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB
import os

def main(q, i, params, tags):
    appname = params['appname']
    connection = OsisDB().getConnection(appname)
    modelDir = q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, "interface", "model")

    if q.system.fs.exists(modelDir):
        for model in q.system.fs.listFilesInDir(modelDir, recursive=True, filter='*.py'):

            parts = model.split(os.sep)
            domain = parts[-2]
            model = parts[-1]
            model = model.split(".")[0]

            connection.createObjectTypeByName(domain, model)
