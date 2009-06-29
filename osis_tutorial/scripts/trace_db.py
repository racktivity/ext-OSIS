from pymonkey import q
from trace_imports import *

q.qshellconfig.interactive = True

#Function to trace function calls and execute them.
def trace_exec(call, args_dict={}, out_var_name=None, wait='True'):
    
    if out_var_name == None:
        print 'command: %s' %call
    else:
        print 'command: ' + out_var_name + ' = %s' %call

    ret_val = eval(call, globals(), args_dict)

    #Wait on user input if required
    if wait == 'True':
        print '\n'
        print 'Press ENTER to continue ....\n'
        q.gui.dialog.askString("")

    return ret_val
