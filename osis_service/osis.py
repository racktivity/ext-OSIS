import os.path 
import functools    

from osis.server.applicationserver import OsisServer

app_root = os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)
model_path = os.path.join(app_root, 'interface', 'pymodel')
tasklet_path = os.path.join(app_root, 'impl', 'osis')  

OsisServer = functools.partial(OsisServer, model_paths=[model_path], tasklet_path=tasklet_path)
