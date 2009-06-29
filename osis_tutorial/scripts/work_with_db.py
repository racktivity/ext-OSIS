from pymonkey import q,i
from trace_db import trace_exec
from osis.model.serializers import ThriftSerializer

q.qshellconfig.interactive = True
args_dict={}

#Function to obtain details of an object with a given guid.
def get_obj(obj_guid):
    
    args_dict['obj_guid'] = obj_guid
    comp = trace_exec('client.company.get(obj_guid)', args_dict, wait='False')
    
    print '\nOBJECT DETAILS:'
    print '==============='
    print 'Name: %s' %comp.name
    print 'URL: %s' %comp.url
    print 'No. of Employees: %d' %len(comp.employees)
    for emp in comp.employees:
        print 'E-mail addresses for \'%s\':' %emp.first_name
	print '----------------------------'
        for e_mail_add in emp.email_addresses:
            print e_mail_add
        print '\n'

print '\nSetting up the XML-RPC transport layer'
port_info = '\'http://localhost:%s\'' %i.servers.applicationserver.getConfig()['xmlrpc_port']
port_info_arg = 'XMLRPCTransport( %s, \'osis_service\')' %port_info 
transport = trace_exec(port_info_arg, out_var_name='transport')
args_dict['transport'] = transport

print '\nCreating client connection with the XML-RPC layer'
client = trace_exec('OsisConnection(transport, ThriftSerializer)', args_dict, 'client')
args_dict['client'] = client

print '\nCreating a new object of type \'Company\' and initializing the same'
company = trace_exec('client.company.new(name=\'Aserver\', url=\'http://www.aserver.com\')', args_dict, 'company', 'False')
args_dict['company'] = company
employee1 = trace_exec('company.employees.new(first_name=\'John\', last_name=\'Doe\')', args_dict, 'employee1', 'False')
args_dict['employee1'] = employee1
trace_exec('employee1.email_addresses.append(\'john.doe@aserver.com\')', args_dict, wait='False')
trace_exec('employee1.email_addresses.append(\'john@aserver.com\')', args_dict, wait='False')
trace_exec('company.employees.append(employee1)', args_dict)

print '\nSaving new object to the database'
trace_exec('client.company.save(company)', args_dict)

print '\nGUID of the saved object: %s' %company.guid

print '\nObtaining values for the saved \'company\' object, based on it\'s guid'
get_obj(company.guid)

print 'Press ENTER to continue .....\n'
q.gui.dialog.askString("")

print '\nQuerying database to obtain \'company\' objects whose name contain \'serv\''
filter_ = trace_exec('client.company.getFilterObject()', args_dict, 'filter_', 'False')
args_dict['filter_'] = filter_
trace_exec('filter_.add(\'name_url\', \'name\', \'serv\') # viewname, fieldname, value', args_dict, wait='False')
guid_list = trace_exec('client.company.find(filter_)', args_dict, 'guid_list', 'False')
args_dict['guid_list'] = guid_list
print '\nNo. of matches : %d' %len(guid_list)
print 'Press ENTER to view details for all matches ......'
q.gui.dialog.askString("")
for guid in guid_list:
    get_obj(guid)

print '\nPress ENTER to see view data for the same query:'
results = trace_exec('client.company.find(filter_, \'name_url\')', args_dict, 'results')
args_dict['results'] = results
count = 1
for result in results._list[1]:
    print '\n DETAILS FOR ROW NO. %d' %count
    print '========================='
    for view_row in result:
        print view_row
    count = count + 1
