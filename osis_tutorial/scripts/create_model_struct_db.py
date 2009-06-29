from pymonkey import q
from trace_db import trace_exec

args_dict={}

print '\nAdding a connection named \'main\'to the \'osis\' database'
osisdb = trace_exec('OsisDB()', out_var_name='osisdb', wait='False')
args_dict['osisdb'] = osisdb
trace_exec('osisdb.addConnection(\'main\', \'127.0.0.1\', \'osis\', \'qbase\', \'pass123\')', args_dict, wait='False')
con = trace_exec('osisdb.getConnection(\'main\')', args_dict, 'con')
args_dict['con'] = con

print 'Creating structure in \'osis\' database for object type \'company\''
trace_exec('con.createObjectTypeByName(\'company\')', args_dict)

print 'Registering a view for the \'company\' object. Name of the view is \'name_url\''
view = trace_exec('con.viewCreate(\'company\', \'name_url\')', args_dict, 'view', 'False')
args_dict['view'] = view
trace_exec('view.setCol(\'name\', q.enumerators.OsisType.STRING, False)', args_dict, wait='False')
trace_exec('view.setCol(\'url\', q.enumerators.OsisType.STRING, False)', args_dict, wait='False')
trace_exec('con.viewAdd(view)', args_dict, wait='False')
