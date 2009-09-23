# <License type="Aserver BSD" version="2.0">
# 
# Copyright (c) 2005-2009, Aserver NV.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
# 
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
# 
# * Neither the name Aserver nor the names of other contributors
#   may be used to endorse or promote products derived from this
#   software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY ASERVER "AS IS" AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL ASERVER BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# </License>

'''Main package for the OSIS library'''

import logging

logger = logging.getLogger('osis') #pylint: disable-msg=C0103

ROOTOBJECT_TYPES = dict()

from osis.model.serializers.osisyaml import YamlSerializer

def init(model_path):
    '''Initialize the OSIS library

    @param model_path: Folder path containing all root object model modules
    @type model_path: string
    '''
    import osis.utils
    import osis.client.connection

    types = list(osis.utils.find_rootobject_types(model_path))
    logger.info('printing all types %s'%str(types) )

    for type_ in types:
        name = type_.__name__
        if name in ROOTOBJECT_TYPES:
            raise RuntimeError('Duplicate root object type %s' % name)
        ROOTOBJECT_TYPES[name] = type_

    osis.client.connection.update_rootobject_accessors()

def prepare_and_send_xml_structure_to_compass(ip,port):
    '''Initialize the OSIS library

    @param model_path: Folder path containing all root object model modules
    @type model_path: string
    '''
    
    import osis.utils
    import osis.client.connection
    import sys
    sys.path.append('/opt/qbase3/apps/kademlia_dht/')
    import dht_client
    ip=str(ip)
    port=int(port)
    dht_client.initialise(ip,port)

    for items in ROOTOBJECT_TYPES:
	logger.info(' sending parameters %s'%ROOTOBJECT_TYPES[items] )
    	rr=YamlSerializer.class_structure_serialize(ROOTOBJECT_TYPES[items])
	logger.info('inside osis , got value %s'%rr)
	dht_client.send_data(ip,port,ROOTOBJECT_TYPES[items].__name__,rr,"4")

    dht_client.disconnect_from_network()



# Set up binding to PyMonkey logging
def _setup_pymonkey_logging():
    '''Relay OSIS log messages to PyMonkey logging if available

    OSIS uses the standard Python *logging* module to perform logging. This
    function makes sure any messages logged to the logging module in the *osis*
    namespace is relayed to the PyMonkey logging subsystem using an appropriate
    loglevel.
    '''
    try:
        from pymonkey import q
    except ImportError:
        logger.info('No PyMonkey support on this system')
        return

    _logging_level_map = {
        logging.CRITICAL: 1,
        logging.ERROR: 2,
        logging.WARNING: 3,
        logging.WARN: 3,
        logging.INFO: 5,
        logging.DEBUG: 6,
        logging.NOTSET: 7,
    }

    class PyMonkeyLogger(logging.Handler):
        '''Basic logging handler which hooks PyMonkey logging to Python
        logging'''
        def emit(self, record):
            '''Emit one logrecord to the PyMonkey logging subsystem'''
            level = _logging_level_map.get(record.levelno, 7)

            q.logger.log('%s%s' % (
                             '[%s] ' % record.name if record.name else '',
                             record.getMessage(),
                         ),
                         level)

    pmlogger = PyMonkeyLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(pmlogger)

_setup_pymonkey_logging()
del _setup_pymonkey_logging
