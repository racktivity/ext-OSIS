from pymonkey import q
from trace_db import trace_exec

args_dict={}

print '\nStarting postgreSQL database server'
trace_exec('q.manage.postgresql8.start()', wait='False')

print '\nAdding database \'osis\' to the server'
trace_exec('q.manage.postgresql8.startChanges()', wait='False')
trace_exec('q.manage.postgresql8.cmdb.addDatabase(\'osis\')', wait='False')
trace_exec('q.manage.postgresql8.save()', wait='False')
trace_exec('q.manage.postgresql8.applyConfig()', wait='False')
