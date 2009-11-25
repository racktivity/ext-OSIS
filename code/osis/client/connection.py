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

'''OSIS client implementation'''

import uuid
import logging

from osis.client.view import ViewResultList
from osis.store.OsisFilterObject import OsisFilterObject

logger = logging.getLogger('osis.client.connection') #pylint: disable-msg=C0103


import os.path
import base64
import logging

from pymonkey import q #pylint: disable-msg=F0401


#################### HACK LOCAL CLIENT ############################

"""
def initialize():
    '''Set up OSIS'''
    osisDir = q.system.fs.joinPaths(q.dirs.baseDir, 'libexec', 'osis')
    q.system.fs.createDir(osisDir)
    from osis import init
    init(osisDir)

initialize()
"""
from osis.server.base import BaseServer
from osis.server.exceptions import ObjectNotFoundException

#
#class LocalClient(BaseServer):
#    """
#    Client bypasssing the XMLRPC stack
#    """
#
#    def __init__(self, transport, serializer, tasklet_path=None):
#        '''Initialize the OSIS service
#
#        @param tasklet_path: Container path of OSIS tasklets
#        @type tasklet_path: string
#        '''
#        BaseServer.__init__(self)
#        
#        self.serializer = serializer
#
#        tasklet_path = tasklet_path or \
#                '/opt/qbase3/apps/applicationserver/services/osis_service/tasklets/'
#        self.tasklet_engine = q.getTaskletEngine(tasklet_path)
#
#    def new(self, *args, **kwargs): #pylint: disable-msg=W0142
#        '''Create a new instance of the root object type
#
#        All arguments are handled verbatim to the root object type constructor.
#        '''
#        #pylint: disable-msg=E1101
#        return self._ROOTOBJECTTYPE(*args, **kwargs)
#
#    def get(self, guid, version=None):
#        '''Retrieve an object from the OSIS object store
#
#        @param object_type: Object type name
#        @type object_type: string
#        @param guid: GUID of the object to retrieve
#        @type guid: string
#        @param serializer: Name of the serializer to use
#        @type serializer: string
#
#        @return: Base64 encoded string of the serialized object
#        @rtype: string
#        '''
#        
#        if not version:
#            data = BaseServer.get(self, self._ROOTOBJECTTYPE.__name__, guid,
#                                      self.serializer.NAME)
#        else:
#            data = self.get_version(self._ROOTOBJECTTYPE.__name__,
#                                              guid, version,
#                                              self.serializer.NAME)
#
#        return self._ROOTOBJECTTYPE.deserialize(self.serializer, data)
#
#    def get_version(self, objectType, guid, version, serializer):
#        '''Retrieve a specific version of an object from the OSIS object store
#
#        @param object_type: Object type name
#        @type object_type: string
#        @param guid: GUID of the object to retrieve
#        @type guid: string
#        @param version: Version GUID of the object to retrieve
#        @type version: string
#        @param serializer: Name of the serializer to use
#        @type serializer: string
#
#        @return: Base64 encoded string of the serialized object
#        @rtype: string
#        '''
#        data = BaseServer.get_version(self, objectType, guid, version,
#                                      self.serializer)
#
#        return self._ROOTOBJECTTYPE.deserialize(self.serializer, data)
#
#    def query(self, Query):
#        ''' run query from OSIS server
#
#        @param query: Query to execute on OSIS server
#        @type query: string
#    
#        @return: result of the query else raise error
#        @type: List of rows. Each row shall be represented as a dictionary.
#        '''
#
#        return self.runQuery(Query)
#
#    def runQuery(self, query):
#        '''Run query from OSIS server
#
#        @param query: Query to execute on OSIS server
#        @type query: string
#
#        @return: result of the query else raise error
#        @type: List of rows. Each row shall be represented as a dictionary.
#        '''
#
#    # Set up tasklet call parameters
#        params = {'query': query}
#        self.tasklet_engine.execute(params=params, tags=('osis', 'query'))
#        if not 'result' in params or not params['result']:
#            return list()
#
#        return params['result']
#
#
#    def delete(self, guid, version=None):
#        '''Delete an object from the OSIS object store
#
#        @param object_type: Object type name
#        @type object_type: string
#        @param guid: GUID of the object to delete
#        @type guid: string
#
#        @return: True or False, according as deletion succeeds or fails.
#        '''
#        
#        # Set up tasklet call parameters
#        params = {
#             'rootobjectguid': guid,
#             'rootobjecttype': self._ROOTOBJECTTYPE.__name__,
#             'rootobjectversionguid': version
#        }
#
#        self.tasklet_engine.execute(params=params, tags=('osis', 'delete'))
#
#        if not 'result' in params or not params['result']:
#            return False
#
#        return params['result']
#
#    def save(self, object_):
#        '''Save a root object to the server
#
#        @param object_: Object to store
#        @type object_: L{osis.model.RootObjectModel}
#        '''
#        #pylint: disable-msg=E1101
#        type_ = self._ROOTOBJECTTYPE.__name__
#
#        # Check whether we should set a GUID
#        try:
#            guid = object_.guid
#        except AttributeError:
#            guid = None
#        if not guid:
#            object_.guid = str(uuid.uuid4())
#
#        # Set version guid
#        object_.version = str(uuid.uuid4())
#
#        data = object_.serialize(self.serializer)
#        return self.put(type_, data, self.serializer.NAME)
#    
#    def put(self, objectType, data, serializer):
#        '''Save an object in the OSIS object store
#
#        @param objectType: Object type name
#        @type objectType: string
#        @param data: Serialized object
#        @type data: string
#        @param serializer: Name of the serializer to use
#        @type serializer: string
#        '''
#        BaseServer.put(self, objectType, data, serializer)
#        return True
#
#    def find(self, filter_, view=None):
#        '''Perform a find/filter operation
#
#        If no view name is specified, a list of GUIDs of the matching root
#        objects is returned. Otherwise a L{ViewResultList} is returned.
#
#        @param filter_: Filter description
#        @type filter_: OsisFilterObject
#        @param view: View to return
#        @type view: string
#
#        @return: List of GUIDs or view result
#        @rtype: tuple<string> or L{ViewResultList}
#        '''
#        #pylint: disable-msg=E1101
#        type_ = self._ROOTOBJECTTYPE.__name__
#
#        result = BaseServer.find(self, type_, filter_.filters, view)
#
#        if not view:
#            return result
#        else:
#            return ViewResultList(result)
#
#    
#    def findAsView(self, filter_, viewName):
#        """
#        Perform a find/filter operation.
#        @param filter_: Filter description
#            @type filter_: OsisFilterObject
#            @param view: name of the view to return
#            @type view: string
#    
#        @return: list of dicts representing the view{col: value}
#        """
#        type_ = self._ROOTOBJECTTYPE.__name__
#
#        
#        return BaseServer.findAsView(self, type_, filter_.filters, viewName)
#
#    #pylint: disable-msg=W0613
#    def get_object_from_store(self, object_type, guid, preferred_serializer,
#                              version=None):
#        '''Retrieve an object from the store
#
#        @param object_type: Object type name
#        @type object_type: string
#        @param guid: GUID of the object to retrieve
#        @type guid: string
#        @param preferred_serializer: The preferred serializer type name
#                                     If this is given and the store stores
#                                     objects using this serialization format, no
#                                     deserialization is required and the
#                                     serialized form can be returned as-is.
#        @type preferred_serializer: string
#        @param version: Version of the object to retrieve
#        @type version: string
#
#        @return: Tuple containing the deserialized object and its serialized
#                 form according to C{preferred_serializer}, where one of the two
#                 items is C{None}: the object if the serialized form could be
#                 returned, the serialized form if it is not available but the
#                 deserialized object is given instead.
#        @rtype: tuple<object, string>
#
#        @raise ObjectNotFoundException: The object could not be found
#        '''
#        # Set up tasklet call parameters
#        params = {
#            'rootobjectguid': guid,
#            'rootobjecttype': object_type,
#            'rootobjectversionguid': version,
#        }
#
#        # Call tasklets. In the end, 'rootobject' should be in params
#        self.tasklet_engine.execute(params=params, tags=('osis', 'get', ))
#
#        if not 'rootobject' in params:
#            raise ObjectNotFoundException('Object %s with guid %s '
#                                          'not found' % (object_type, guid))
#
#        return params['rootobject'], None
#
#    def put_object_in_store(self, object_type, object_):
#        '''Store an object in the store
#
#        @param object_type: Object type name
#        @type object_type: string
#        @param object_: The object to store
#        @type object_: object
#        '''
#        # Execute store taslkets
#        params = {
#            'rootobject': object_,
#            'rootobjecttype': object_type,
#        }
#
#
#        self.tasklet_engine.execute(params=params, tags=('osis', 'store',))
#
#
#    def execute_filter_as_view(self, object_type, filter_, view):
#        '''Execute a query on the store
#
#        @param object_type: Object type name
#        @type object_type: string
#        @param filter_: Filter to execute
#        @type filter_: L{Filter}
#        @param view: view name to return
#        @type view: string
#
#        @return: OSISList formatted resultset
#        @rtype: tuple
#        '''
#        params = {
#            'rootobjecttype': object_type,
#            'filterobject': filter_,
#            'osisview': view,
#        }
#
#        self.tasklet_engine.execute(params=params, tags=('osis','findasview'))
#
#        if not 'result' in params or not params['result']:
#            return list()
#
#        return params['result']
#
#    def execute_filter(self, object_type, filter_, view):
#        '''Execute a query on the store
#
#        @param object_type: Object type name
#        @type object_type: string
#        @param filter_: Filter to execute
#        @type filter_: L{Filter}
#        @param view: Optional view name to return
#        @type view: string
#
#        @return: OSISList formatted resultset
#        @rtype: tuple
#        '''
#        params = {
#            'rootobjecttype': object_type,
#            'filterobject': filter_,
#            'osisview': view,
#        }
#
#        self.tasklet_engine.execute(params=params, tags=('osis','findobject'))
#
#        if not 'result' in params or not params['result']:
#            return list()
#
#        return params['result']
#    
#    @staticmethod
#    def getFilterObject(): #pylint: disable-msg=C0103
#        '''Create a new filter object instance'''
#        return OsisFilterObject()

#################### /HACK LOCAL CLIENT ############################



class OsisClient(object):
    '''Client class to handle one root object type on a server

    An extra attribute, C{_ROOTOBJECTTYPE}, is virtual and should be set in
    subclasses.
    '''
    def __init__(self, transport, serializer):
        '''Initialize a new OSIS root object client

        @param transport: OSIS client transport
        @type transport: object
        @param serializer: Object serializer implementation
        @type serializer: object
        '''
        self.transport = transport
        self.serializer = serializer

    def get(self, guid, version=None):
        '''Retrieve a root object with a given GUID from the OSIS server

        If no version is specified, the latest version is retrieved.

        @param guid: GUID of the root object to retrieve
        @type guid: string
        @param version: Version GUID of the object to retrieve
        @type version: string

        @return: Root object instance
        @rtype: L{osis.model.RootObjectModel}
        '''
        #pylint: disable-msg=E1101
        if not version:
            data = self.transport.get(self._ROOTOBJECTTYPE.__name__, guid,
                                      self.serializer.NAME)
        else:
            data = self.transport.get_version(self._ROOTOBJECTTYPE.__name__,
                                              guid, version,
                                              self.serializer.NAME)
        return self._ROOTOBJECTTYPE.deserialize(self.serializer, data)


    def query(self, Query):
        ''' run query from OSIS server

    	@param query: Query to execute on OSIS server
    	@type query: string
    
    	@return: result of the query else raise error
    	@type: List of rows. Each row shall be represented as a dictionary.
    	'''
    
    	return self.transport.runQuery(Query)

    def delete(self, guid, version=None):
        '''Delete a root object with a given GUID from the OSIS server

        If no version is specified, all the versions shall be deleted.

        @param guid: GUID of the root object to delete
        @type guid: string
        @param version: Version GUID of the object to delete
        @type version: string

        @return: True or False, according as the deletion succeeds or fails
        '''
        if not version:
            return self.transport.delete(self._ROOTOBJECTTYPE.__name__, guid)
        else:
            return self.transport.delete_version(self._ROOTOBJECTTYPE.__name__,
                                                 guid, version)

    def save(self, object_):
        '''Save a root object to the server

        @param object_: Object to store
        @type object_: L{osis.model.RootObjectModel}
        '''
        #pylint: disable-msg=E1101
        type_ = self._ROOTOBJECTTYPE.__name__

        # Check whether we should set a GUID
        try:
            guid = object_.guid
        except AttributeError:
            guid = None
        if not guid:
            object_.guid = str(uuid.uuid4())

        # Set version guid
        object_.version = str(uuid.uuid4())

        data = object_.serialize(self.serializer)
        return self.transport.put(type_, data, self.serializer.NAME)

    def new(self, *args, **kwargs): #pylint: disable-msg=W0142
        '''Create a new instance of the root object type

        All arguments are handled verbatim to the root object type constructor.
        '''
        #pylint: disable-msg=E1101
        return self._ROOTOBJECTTYPE(*args, **kwargs)

    @staticmethod
    def getFilterObject(): #pylint: disable-msg=C0103
        '''Create a new filter object instance'''
        return OsisFilterObject()

    def find(self, filter_, view=None):
        '''Perform a find/filter operation

        If no view name is specified, a list of GUIDs of the matching root
        objects is returned. Otherwise a L{ViewResultList} is returned.

        @param filter_: Filter description
        @type filter_: OsisFilterObject
        @param view: View to return
        @type view: string

        @return: List of GUIDs or view result
        @rtype: tuple<string> or L{ViewResultList}
        '''
        #pylint: disable-msg=E1101
        type_ = self._ROOTOBJECTTYPE.__name__

        result = self.transport.find(type_, filter_, view)

        if not view:
            return result
        else:
            return ViewResultList(result)

    def findAsView(self, filter_, viewName):
    	"""
    	Perform a find/filter operation.
    	@param filter_: Filter description
            @type filter_: OsisFilterObject
            @param view: name of the view to return
            @type view: string
    
    	@return: list of dicts representing the view{col: value}
    	"""
    	type_ = self._ROOTOBJECTTYPE.__name__

        result = self.transport.findAsView(type_, filter_, viewName)

        return result

class OsisConnection(object):
    '''Connection to an OSIS server

    This method provides a connection to an OSIS server, using a given transport
    instance.
    '''
    #pylint: disable-msg=R0903
    def __init__(self, transport, serializer):
        '''Initialize a client

        @param transport: OSIS client transport
        @type transport: object
        @param serializer: Object serializer implementation
        @type serializer: object
        '''
        self._accessors = dict()
        self.transport = transport
        self.serializer = serializer


class RootObjectAccessor(object): #pylint: disable-msg=R0903
    '''Descriptor returning a correct L{OsisClient} instance for every root
    object exposed on L{OsisConnection}

    Every L{OsisConnection} instance got an attribute, C{_accessors}, which, for
    every root object type, can contain an L{OsisClient} instance which will
    provide the necessary methods to retrieve the corresponding root objects
    from the server.
    '''
    def __init__(self, name, type_):
        '''Initialize a new root object accessor

        @param name: Name of the accessor ('clients' in 'connection.clients')
        @type name: string
        @param type_: Root object type to provide access to
        @type type_: type
        '''
        logger.info('Creating root object accessor %s' % name)

        self._name = name

        #class AccessorImpl(OsisClient):
        class AccessorImpl(OsisClient):
            '''Implementation of an specific L{OsisClient} root object
            accessor'''
            _ROOTOBJECTTYPE = type_

        self._accessorimpl = AccessorImpl

    def __get__(self, obj, type_=None): #pylint: disable-msg=W0613
        '''Retrieve the accessor from a connection object'''
        #pylint: disable-msg=W0212
        accessor = obj._accessors.get(self._name, None)
        if not accessor or not isinstance(accessor, self._accessorimpl):
            accessor = self._accessorimpl(obj.transport, obj.serializer)
            obj._accessors[self._name] = accessor

        return accessor


def update_rootobject_accessors():
    '''Update the L{OsisConnection} class so all root object types are
    accessible

    Whenever the L{osis.ROOTOBJECT_TYPES} dictionary is updated, this function
    should be called so the corresponding attributes on the L{OsisConnection}
    class can be set up.
    '''
    logger.info('Updating known RootObjectModel types')

    from osis import ROOTOBJECT_TYPES as types

    # Remove all existing accessors
    for attrname in dir(OsisConnection):
        attr = OsisConnection.__dict__.get(attrname, None)
        if attr and isinstance(attr, RootObjectAccessor):
            logger.debug('Removing old type %s' % attrname)
            delattr(OsisConnection, attrname)

    # Now add all of them again
    for type_ in types.itervalues():
        name = getattr(type_, 'OSIS_TYPE_NAME', type_.__name__.lower())
        accessor = RootObjectAccessor(name, type_)
        logger.debug('Adding new type %s' % name)
        setattr(OsisConnection, name, accessor)
