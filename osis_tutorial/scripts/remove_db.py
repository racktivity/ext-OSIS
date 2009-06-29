from pymonkey import q
from trace_db import trace_exec

args_dict={}

print '\nRemoving database \'osis\' from the server'
trace_exec('q.manage.postgresql8.startChanges()', wait='False')
trace_exec('q.manage.postgresql8.cmdb.removeDatabase(\'osis\')', wait='False')
trace_exec('q.manage.postgresql8.save()', wait='False')
trace_exec('q.manage.postgresql8.applyConfig()', wait='False')

print '\nStopping postgreSQL database server'
trace_exec('q.manage.postgresql8.stop()', wait='False')

