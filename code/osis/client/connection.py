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

    def get(self, guid):
        '''Retrieve a root object with a given GUID from the OSIS server

        If no version is specified, the latest version is retrieved.

        @param guid: GUID of the root object to retrieve
        @type guid: string
        
        @return: Root object instance
        @rtype: L{osis.model.RootObjectModel}
        '''
        #pylint: disable-msg=E1101
        data = self.transport.get(self._domain, self._ROOTOBJECTTYPE.__name__, guid,
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

    def delete(self, guid):
        '''Delete a root object with a given GUID from the OSIS server

        If no version is specified, all the versions shall be deleted.

        @param guid: GUID of the root object to delete
        @type guid: string
        
        @return: True or False, according as the deletion succeeds or fails
        '''
        return self.transport.delete(self._domain, self._ROOTOBJECTTYPE.__name__, guid)
        
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
        
        # Keep original version to be able to check for concurrency violations    
        object_._baseversion = object_.version

        # Set version guid
        object_.version = str(uuid.uuid4())

        data = object_.serialize(self.serializer)
        
        result = self.transport.put(self._domain, type_, data, self.serializer.NAME)
        
        # If everything is ok, set baseversion to version 
        object_._baseversion = object_.version
        
        return result

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

        result = self.transport.find(self._domain, type_, filter_, view)

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
        result = self.transport.findAsView(self._domain, type_, filter_, viewName)
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

class AccessorImpl(OsisClient):
        '''Implementation of an specific L{OsisClient} root object
        accessor'''
        pass

class RootObjectAccessor(object): #pylint: disable-msg=R0903
    '''Descriptor returning a correct L{OsisClient} instance for every root
    object exposed on L{OsisConnection}

    Every L{OsisConnection} instance got an attribute, C{_accessors}, which, for
    every root object type, can contain an L{OsisClient} instance which will
    provide the necessary methods to retrieve the corresponding root objects
    from the server.
    '''


    def __init__(self, name, type_, clientClass=AccessorImpl):
        '''Initialize a new root object accessor

        @param name: Name of the accessor ('clients' in 'connection.clients')
        @type name: string
        @param type_: Root object type to provide access to
        @type type_: type
        '''
        logger.info('Creating root object accessor %s' % name)
        self._name = name
        class AccessorImpl_(clientClass):
            '''Implementation of an specific L{OsisClient} root object
            accessor'''
            _ROOTOBJECTTYPE = type_

        self._accessorimpl = AccessorImpl_

    def __get__(self, domain, type_=None): #pylint: disable-msg=W0613
        '''Retrieve the accessor from a connection object'''
        #pylint: disable-msg=W0212
        client = domain._parent
        accessor = client._accessors.get(self._name, None)
        if not accessor or not isinstance(accessor, self._accessorimpl):
            accessor = self._accessorimpl(client.transport, client.serializer)
            accessor._domain = domain.name
            client._accessors[self._name] = accessor

        return accessor

class DomainAccessor(object):
    '''Dummy object to group RootObjectAccessors per domain'''
    
    def __init__(self, name):
        self.name = name
    
    def __get__(self, client, type_=None): #pylint: disable-msg=W0613
        '''Make sure we know through which object we are being accessed'''
        #pylint: disable-msg=W0212
        self._parent = client
        return self

def update_rootobject_accessors(cls, clientClass):
    '''Update the L{OsisConnection} class so all root object types are
    accessible

    Whenever the L{osis.ROOTOBJECT_TYPES} dictionary is updated, this function
    should be called so the corresponding attributes on the L{OsisConnection}
    class can be set up.
    '''
    logger.info('Updating known RootObjectModel types')

    from pymodel import ROOTOBJECT_TYPES as types

    ## Remove old accessors
    for attrname in dir(cls):
        attr = cls.__dict__.get(attrname, None)
        if attr and isinstance(attr, RootObjectAccessor) and not any([attrname == getattr(type_,  'PYMODEL_TYPE_NAME', type_.__name__.lower()) for type_ in types.itervalues()]):
            logger.debug('Removing old type %s' % attrname)
            delattr(cls, attrname)

    # update accessors
    for domain_name, domain_ in types.iteritems():
        
        domain_acc = DomainAccessor(domain_name)
        
        for type_ in domain_.itervalues():
            name = getattr(type_, 'PYMODEL_TYPE_NAME', type_.__name__.lower())
            accessor = RootObjectAccessor(name, type_, clientClass)
            logger.debug('Adding new type %s' % name)
            setattr(DomainAccessor, name, accessor)
            
        setattr(cls, domain_name, domain_acc)
