# <License type="Sun Cloud Commercial" version="2.0">
# 
# Copyright (C) 2005-2009, Sun Microsystems, Inc.
# All rights reserved.
# 
# This file is subject to the Sun EULA.
# 
# ALTHOUGH YOU MAY BE ABLE TO READ THE CONTENT OF THIS FILE,
# THIS FILE CONTAINS CONFIDENTIAL INFORMATION OF SUN MICROSYSTEMS INC.
# YOU ARE NOT ALLOWED TO MODIFY, PUBLISH OR DISTRIBUTE ITS CONTENT,
# EMBED IT IN OTHER SOFTWARE, OR CREATE DERIVATIVE WORKS.
# 
# For more information, please consult the Sun EULA or the
# LICENSE.TXT file (both contained in the "LICENSES" folder of
# this package).
# 
# </License>
 
__tags__= 'nephos', 'type_MACHINE', ('create','update') , 'rootobject', 'qlayer', 'PORTAL'
__author__='aserver'
__realizes__ = 'cloudcentral_machine'



def main(q,i,params,tags):   
    '''
    Generate the wiki page for a machine
    '''
    
    try:
        q.logger.log('generate machine page',3)
        q.qlayer.qportal.generatePage('', 'bo/9876-543-2/machines/1234-567-8', 'cloudcentral_machine',  {'machine': None , 'boxoffice': None})
        q.logger.log('done',3)
        
    except Exception, e:
        q.logger.log('ERROR in cloudcentral_machine tasklet : %s'%str(e), 3)
        
def match(q,i,params,tags):
    '''
    Check if this tasklet is applicable to the rootobject
    '''    
    return True
