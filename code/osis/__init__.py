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
from client.connection import AccessorImpl
from client.connection import OsisConnection
import osis

logger = logging.getLogger('osis') #pylint: disable-msg=C0103

#ROOTOBJECT_TYPES = dict()

def init(connectionClass=OsisConnection, clientClass=AccessorImpl):
    '''Initialize the OSIS library'''
    osis.client.connection.update_rootobject_accessors(connectionClass, clientClass)


## Set up binding to PyMonkey logging
#def _setup_pylabs_logging():
#    '''Relay OSIS log messages to PyMonkey logging if available
#
#    OSIS uses the standard Python *logging* module to perform logging. This
#    function makes sure any messages logged to the logging module in the *osis*
#    namespace is relayed to the PyMonkey logging subsystem using an appropriate
#    loglevel.
#    '''
#    try:
#        from pylabs import q
#    except ImportError:
#        logger.info('No PyMonkey support on this system')
#        return
#
#    _logging_level_map = {
#        logging.CRITICAL: 1,
#        logging.ERROR: 2,
#        logging.WARNING: 3,
#        logging.WARN: 3,
#        logging.INFO: 5,
#        logging.DEBUG: 6,
#        logging.NOTSET: 7,
#    }
#
#    class PyMonkeyLogger(logging.Handler):
#        '''Basic logging handler which hooks PyMonkey logging to Python
#        logging'''
#        def emit(self, record):
#            '''Emit one logrecord to the PyMonkey logging subsystem'''
#            level = _logging_level_map.get(record.levelno, 7)
#
#            q.logger.log('%s%s' % (
#                             '[%s] ' % record.name if record.name else '',
#                             record.getMessage(),
#                         ),
#                         level)
#
#    pmlogger = PyMonkeyLogger()
#    logger.setLevel(logging.DEBUG)
#    logger.addHandler(pmlogger)
#
#_setup_pylabs_logging()
#del _setup_pylabs_logging
