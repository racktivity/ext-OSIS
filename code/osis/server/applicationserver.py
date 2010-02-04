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

from pymonkey import q #pylint: disable-msg=F0401

from osis.server.base import BaseServer
from osis.server.exceptions import ObjectNotFoundException

def initialize():
    '''Set up OSIS'''
    osisDir = q.system.fs.joinPaths(q.dirs.baseDir, 'libexec', 'osis')
    q.system.fs.createDir(osisDir)
    from osis import init
    init(osisDir)

initialize()

logger = logging.getLogger('osis.server.applicationserver')

class OsisServer(BaseServer):
    '''Implementation of an OSIS server running in the PyMonkey
    Applicationserver'''

    def __init__(self, tasklet_path=None):
        '''Initialize the OSIS service

        @param tasklet_path: Container path of OSIS tasklets
        @type tasklet_path: string
        '''
        BaseServer.__init__(self)

        tasklet_path = tasklet_path or \
                os.path.join(os.path.dirname(__file__), 'tasklets')
        self.tasklet_engine = q.getTaskletEngine(tasklet_path)

    @q.manage.applicationserver.expose
    def get(self, objectType, guid, serializer):
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
        data = BaseServer.get(self, objectType, guid, serializer)
        # Encode serialized object using Base64
        return base64.encodestring(data)

    @q.manage.applicationserver.expose
    def get_version(self, objectType, guid, version, serializer):
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
        data = BaseServer.get_version(self, objectType, guid, version,
                                      serializer)
        # Encode serialized object using Base64
        return base64.encodestring(data)


    @q.manage.applicationserver.expose
    def runQuery(self, query):
        '''Run query from OSIS server

        @param query: Query to execute on OSIS server
        @type query: string

        @return: result of the query else raise error
        @type: List of rows. Each row shall be represented as a dictionary.
        '''

	# Set up tasklet call parameters
    	params = {'query': query}
    	self.tasklet_engine.execute(params=params, tags=('osis', 'query'))
	if not 'result' in params or not params['result']:
            return list()

        return params['result']


    @q.manage.applicationserver.expose
    def delete(self, objectType, guid):
        '''Delete an object from the OSIS object store

        @param object_type: Object type name
        @type object_type: string
        @param guid: GUID of the object to delete
        @type guid: string

        @return: True or False, according as deletion succeeds or fails.
        '''
        # Set up tasklet call parameters
        params = {
             'rootobjectguid': guid,
             'rootobjecttype': objectType,
             'rootobjectversionguid': None
        }

        self.tasklet_engine.execute(params=params, tags=('osis', 'delete'))

        if not 'result' in params or not params['result']:
            return False

        return params['result']


    @q.manage.applicationserver.expose
    def delete_version(self, objectType, guid, version):
        '''Delete a specific version of an object from the OSIS object store

        @param object_type: Object type name
        @type object_type: string
        @param guid: GUID of the object to delete
        @type guid: string
        @param version: Version GUID of the object to delete
        @type version: string

        @return: True or False, according as deletion succeeds or fails.
        '''
        # Set up tasklet call parameters
        params = {
            'rootobjectguid': guid,
            'rootobjecttype': objectType,
            'rootobjectversionguid': version
        }

        self.tasklet_engine.execute(params=params, tags=('osis', 'delete'))


        if not 'result' in params or not params['result']:
            return False

        return params['result']

    @q.manage.applicationserver.expose
    def put(self, objectType, data, serializer):
        '''Save an object in the OSIS object store

        @param objectType: Object type name
        @type objectType: string
        @param data: Serialized object
        @type data: string
        @param serializer: Name of the serializer to use
        @type serializer: string
        '''
        # Decode Base64-encoded data
        data = base64.decodestring(data)
        BaseServer.put(self, objectType, data, serializer)
        return True

    @q.manage.applicationserver.expose
    def find(self, objectType, filters, view=''):
        """
        @param objectType: type of the object
        @param filters: filters. list of dicts
        @param view: view to return
        """
        return BaseServer.find(self, objectType, filters, view)


    @q.manage.applicationserver.expose
    def findAsView(self, objectType, filters, view):
        """
        @param objectType: type of the object
        @param filters: filters. list of dicts
        @param view: view to return
        """
        return BaseServer.findAsView(self, objectType, filters, view)

    #pylint: disable-msg=W0613
    def get_object_from_store(self, object_type, guid, preferred_serializer,
                              version=None):
        '''Retrieve an object from the store

        @param object_type: Object type name
        @type object_type: string
        @param guid: GUID of the object to retrieve
        @type guid: string
        @param preferred_serializer: The preferred serializer type name
                                     If this is given and the store stores
                                     objects using this serialization format, no
                                     deserialization is required and the
                                     serialized form can be returned as-is.
        @type preferred_serializer: string
        @param version: Version of the object to retrieve
        @type version: string

        @return: Tuple containing the deserialized object and its serialized
                 form according to C{preferred_serializer}, where one of the two
                 items is C{None}: the object if the serialized form could be
                 returned, the serialized form if it is not available but the
                 deserialized object is given instead.
        @rtype: tuple<object, string>

        @raise ObjectNotFoundException: The object could not be found
        '''
        # Set up tasklet call parameters
        params = {
            'rootobjectguid': guid,
            'rootobjecttype': object_type,
            'rootobjectversionguid': version,
        }

        # Call tasklets. In the end, 'rootobject' should be in params
        self.tasklet_engine.execute(params=params, tags=('osis', 'get', ))

        if not 'rootobject' in params:
            raise ObjectNotFoundException('Object %s with guid %s '
                                          'not found' % (object_type, guid))

        return params['rootobject'], None

    def put_object_in_store(self, object_type, object_):
        '''Store an object in the store

        @param object_type: Object type name
        @type object_type: string
        @param object_: The object to store
        @type object_: object
        '''
        # Execute store taslkets
        params = {
            'rootobject': object_,
            'rootobjecttype': object_type,
        }


        self.tasklet_engine.execute(params=params, tags=('osis', 'store',))


    def execute_filter_as_view(self, object_type, filter_, view):
	'''Execute a query on the store

        @param object_type: Object type name
        @type object_type: string
        @param filter_: Filter to execute
        @type filter_: L{Filter}
        @param view: view name to return
        @type view: string

        @return: OSISList formatted resultset
        @rtype: tuple
        '''
	params = {
            'rootobjecttype': object_type,
            'filterobject': filter_,
            'osisview': view,
        }

        self.tasklet_engine.execute(params=params, tags=('osis','findasview'))

        if not 'result' in params or not params['result']:
            return list()

        return params['result']

    def execute_filter(self, object_type, filter_, view):
        '''Execute a query on the store

        @param object_type: Object type name
        @type object_type: string
        @param filter_: Filter to execute
        @type filter_: L{Filter}
        @param view: Optional view name to return
        @type view: string

        @return: OSISList formatted resultset
        @rtype: tuple
        '''
        params = {
            'rootobjecttype': object_type,
            'filterobject': filter_,
            'osisview': view,
        }

        self.tasklet_engine.execute(params=params, tags=('osis','findobject'))

        if not 'result' in params or not params['result']:
            return list()

        return params['result']
