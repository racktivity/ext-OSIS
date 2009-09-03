import os.path 
import functools    
import pkg_resources   

#pkg_resources.require('osis')    
tasklet_path = os.path.join(os.path.dirname(__file__), 'tasklets')  
from osis.server.applicationserver import OsisServer    
OsisServer = functools.partial(OsisServer, tasklet_path=tasklet_path)
