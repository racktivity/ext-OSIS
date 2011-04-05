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

#pylint: disable-msg=C0103, R0201

'''OSIS server implementation running in the PyMonkey Applicationserver'''

import os.path
import base64
import logging

from pylabs import q #pylint: disable-msg=F0401

from osis.server import base

logger = logging.getLogger('osis.server.applicationserver')

try:
    expose = q.manage.applicationserver.expose
except AttributeError:
    expose = lambda fun: fun

# Do *not* flip inheritance order!
class OsisServer(base.TaskletBasedMixin, base.BaseServer):
    '''Implementation of an OSIS server running in the PyMonkey
    Applicationserver'''

    def __init__(self, models, tasklet_path=None):
        '''Initialize the OSIS service

        @param models: Iterable of (object_type, model) definitions
        @type models: iterable
        @param tasklet_path: Container path of OSIS tasklets
        @type tasklet_path: string
        '''
        base.BaseServer.__init__(self, models)

        tasklet_path = tasklet_path or \
            os.path.join(os.path.dirname(__file__), 'tasklets')
        self.tasklet_engine = q.taskletengine.get(tasklet_path)

    @expose
    def get(self, object_type, guid, serializer):
        '''Retrieve an object from the OSIS object store

        @param object_type: Object type name
        @type object_type: string
        @param guid: GUID of the object to retrieve
        @type guid: string
        @param serializer: Name of the serializer to use
        @type serializer: string

        @return: Base64 encoded string of the serialized object
        @rtype: string
        '''
        data = base.BaseServer.get(self, object_type, guid, serializer)
        # Encode serialized object using Base64
        return base64.encodestring(data)

    @expose
    def get_version(self, object_type, guid, version, serializer):
        '''Retrieve a specific version of an object from the OSIS object store

        @param object_type: Object type name
        @type object_type: string
        @param guid: GUID of the object to retrieve
        @type guid: string
        @param version: Version GUID of the object to retrieve
        @type version: string
        @param serializer: Name of the serializer to use
        @type serializer: string

        @return: Base64 encoded string of the serialized object
        @rtype: string
        '''
        data = base.BaseServer.get_version(self, object_type, guid, version,
            serializer)

        # Encode serialized object using Base64
        return base64.encodestring(data)


    @expose
    def runQuery(self, query):
        '''Run query from OSIS server

        @param query: Query to execute on OSIS server
        @type query: string

        @return: result of the query else raise error
        @type: List of rows. Each row shall be represented as a dictionary.
        '''
        return base.BaseServer.run_query(self, query)

    @expose
    def delete(self, object_type, guid):
        '''Delete an object from the OSIS object store

        @param object_type: Object type name
        @type object_type: string
        @param guid: GUID of the object to delete
        @type guid: string

        @return: True or False, according as deletion succeeds or fails.
        '''
        return base.BaseServer.delete(self, object_type, guid)

    @expose
    def delete_version(self, object_type, guid, version):
        '''Delete a specific version of an object from the OSIS object store

        @param object_type: Object type name
        @type object_type: string
        @param guid: GUID of the object to delete
        @type guid: string
        @param version: Version GUID of the object to delete
        @type version: string

        @return: True or False, according as deletion succeeds or fails.
        '''
        return base.BaseServer.delete_version(self, object_type, guid, version)

    @expose
    def put(self, object_type, data, serializer):
        '''Save an object in the OSIS object store

        @param object_type: Object type name
        @type object_type: string
        @param data: Serialized object
        @type data: string
        @param serializer: Name of the serializer to use
        @type serializer: string
        '''
        # Decode Base64-encoded data
        data = base64.decodestring(data)
        base.BaseServer.put(self, object_type, data, serializer)

        return True

    @expose
    def find(self, object_type, filters, view=''):
        """
        @param object_type: type of the object
        @param filters: filters. list of dicts
        @param view: view to return
        """
        return base.BaseServer.find(self, object_type, filters, view)

    @expose
    def findAsView(self, object_type, filters, view):
        """
        @param objectType: type of the object
        @param filters: filters. list of dicts
        @param view: view to return
        """
        return base.BaseServer.findAsView(self, object_type, filters, view)
