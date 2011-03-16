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

from osis.server.base import BaseServer
from osis.server.exceptions import ObjectNotFoundException

#TODO fix me
for dir in q.system.fs.listDirsInDir(q.dirs.appDir):
    modeldir = q.system.fs.joinPaths(dir, 'model')
    if q.system.fs.exists(modeldir):
        domain = q.system.fs.getBaseName(dir)
        q.pymodel.importDomain(domain, modeldir)

logger = logging.getLogger('osis.server.applicationserver')

class OsisServer(BaseServer):
    '''Implementation of an OSIS server running in the PyMonkey
    Applicationserver'''

    def __init__(self, tasklet_path=None):
        '''Initialize the OSIS service

        @param tasklet_path: Container path of OSIS tasklets
        @type tasklet_path: string
        '''
        BaseServer.__init__(self, tasklet_path)

    @q.manage.applicationserver.expose
    def get(self, domain, objectType, guid, serializer):
        '''Retrieve an object from the OSIS object store

        @param domain: Domain of the object
        @type domain: string
        @param object_type: Object type name
        @type object_type: string
        @param guid: GUID of the object to retrieve
        @type guid: string
        @param serializer: Name of the serializer to use
        @type serializer: string

        @return: Base64 encoded string of the serialized object
        @rtype: string
        '''
        data = BaseServer.get(self, domain, objectType, guid, serializer)
        # Encode serialized object using Base64
        return base64.encodestring(data)

    @q.manage.applicationserver.expose
    def get_version(self, domain, objectType, guid, version, serializer):
        '''Retrieve a specific version of an object from the OSIS object store

        @param domain: Domain of the object
        @type domain: string
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
        data = BaseServer.get_version(self, domain, objectType, guid, version,
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
        
        return BaseServer.runQuery(self, query)

    @q.manage.applicationserver.expose
    def delete(self, domain, objectType, guid):
        '''Delete an object from the OSIS object store

        @param domain: Domain of the object
        @type domain: string
        @param object_type: Object type name
        @type object_type: string
        @param guid: GUID of the object to delete
        @type guid: string

        @return: True or False, according as deletion succeeds or fails.
        '''
        
        return BaseServer.delete(self, domain, objectType, guid)
        
    @q.manage.applicationserver.expose
    def delete_version(self, domain, objectType, guid, version):
        '''Delete a specific version of an object from the OSIS object store

        @param domain: Domain of the object
        @type domain: string
        @param object_type: Object type name
        @type object_type: string
        @param guid: GUID of the object to delete
        @type guid: string
        @param version: Version GUID of the object to delete
        @type version: string

        @return: True or False, according as deletion succeeds or fails.
        '''
        
        return BaseServer.delete_version(self, domain, objectType, guid, version)
    
    @q.manage.applicationserver.expose
    def put(self, domain, objectType, data, serializer):
        '''Save an object in the OSIS object store

        @param domain: Domain of the object
        @type domain: string
        @param objectType: Object type name
        @type objectType: string
        @param data: Serialized object
        @type data: string
        @param serializer: Name of the serializer to use
        @type serializer: string
        '''
        # Decode Base64-encoded data
        data = base64.decodestring(data)
        BaseServer.put(self, domain, objectType, data, serializer)
        return True

    @q.manage.applicationserver.expose
    def find(self, domain, objectType, filters, view=''):
        """
        @param domain: Domain of the object
        @type domain: string
        @param objectType: type of the object
        @param filters: filters. list of dicts
        @param view: view to return
        """
        return BaseServer.find(self, domain, objectType, filters, view)

    @q.manage.applicationserver.expose
    def findAsView(self, domain, objectType, filters, view):
        """

        @param domain: Domain of the object
        @type domain: string
        @param objectType: type of the object
        @param filters: filters. list of dicts
        @param view: view to return
        """
        return BaseServer.findAsView(self, domain, objectType, filters, view)

    #pylint: disable-msg=W0613
    def get_object_from_store(self, domain, object_type, guid, preferred_serializer,
                              version=None):
        '''Retrieve an object from the store

        @param domain: Domain of the object
        @type domain: string
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
        
        return BaseServer.get_object_from_store(self, domain, object_type, guid, preferred_serializer, version)
        
    def put_object_in_store(self, domain, object_type, object_):
        '''Store an object in the store

        @param domain: Domain of the object
        @type domain: string
        @param object_type: Object type name
        @type object_type: string
        @param object_: The object to store
        @type object_: object
        '''
        
        BaseServer.put_object_in_store(self, domain, object_type, object_)


    def execute_filter_as_view(self, domain, object_type, filter_, view):
        '''Execute a query on the store

        @param domain: Domain of the object
        @type domain: string
        @param object_type: Object type name
        @type object_type: string
        @param filter_: Filter to execute
        @type filter_: L{Filter}
        @param view: view name to return
        @type view: string

        @return: OSISList formatted resultset
        @rtype: tuple
        '''
        
        return BaseServer.execute_filter_as_view(self, domain, object_type, filter_, view)
        

    def execute_filter(self, domain, object_type, filter_, view):
        '''Execute a query on the store

        @param domain: Domain of the object
        @type domain: string
        @param object_type: Object type name
        @type object_type: string
        @param filter_: Filter to execute
        @type filter_: L{Filter}
        @param view: Optional view name to return
        @type view: string

        @return: OSISList formatted resultset
        @rtype: tuple
        '''
        
        return BaseServer.execute_filter(self, domain, object_type, filter_, view)
        
