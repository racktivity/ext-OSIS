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
    
import os    

from pymonkey import q

from osis import init
import osis.utils
from osis.model.serializers import ThriftSerializer
from osis.model.serializers import YamlSerializer
from XMLSerializer import XMLSerializer
from ThriftBase64Serializer import ThriftBase64Serializer


from osis.client.xmlrpc import XMLRPCTransport
from osis.client import OsisConnection
from osis.client.connection import *
from osis.store.OsisDB import OsisDB


class Domain(object):
    pass

class PyModelOsisClient(object):
    
    def __init__(self, transport, serializer):
        '''Initialize a new OSIS root object client

        @param transport: OSIS client transport
        @type transport: object
        @param serializer: Object serializer implementation
        @type serializer: object
        '''
        self._transport = transport
        self._serializer = serializer    
    
    def getEmptyModelObject(self, *args, **kwargs):
        return self._ROOTOBJECTTYPE(*args, **kwargs)

    #serializing methods
    def object2XML(self, data):
        return self._serialize(XMLSerializer, data)
    
    def object2YAML(self, data):
        return self._serialize(YamlSerializer, data)
     
    def object2ThriftByteStr(self, data):
        return self._serialize(ThriftSerializer, data)
    
    def object2ThriftBase64Str(self, data):        
        return self._serialize(ThriftBase64Serializer, data)
    
    #deserializing methods
    def XML2object(self, data):
        return self._deserializer(XMLSerializer, data)
    
    def YAML2object(self, data):
        return self._deserializer(YamlSerializer, data)
    
    def thriftByteStr2object(self, data):
        return self._deserializer(ThriftSerializer, data)
    
    def thriftBase64Str2object(self, data):
        return self._deserializer(ThriftBase64Serializer, data)
    
    def _serialize(self, serializer, data):
        return data.serialize(serializer)
    
    def _deserializer(self, serializer, data):
        return self._ROOTOBJECTTYPE.deserialize(serializer, data)
    
class RootPyModelObjectAccessor(RootObjectAccessor):
    
    def __init__(self, name, type_):
        '''Initialize a new root object accessor

        @param name: Name of the accessor ('clients' in 'connection.clients')
        @type name: string
        @param type_: Root object type to provide access to
        @type type_: type
        '''
        logger.info('Creating root object accessor %s' % name)

        self._name = name

        class AccessorImpl(PyModelOsisClient):
            '''Implementation of an specific L{OsisClient} root object
            accessor'''
            _ROOTOBJECTTYPE = type_

        self._accessorimpl = AccessorImpl

class PyModel():

    __shared_state = {}
    
    def __init__(self):
        self.__dict__ = self.__shared_state
        if not hasattr(self, 'initialized'):
            self.__initialize()
            setattr(self, 'initialized', True)
            
    def _initFromPath(self, model_path):
        '''Initialize the OSIS library
            
        @param model_path: Folder path containing all root object model modules
        @type model_path: string
        '''
        types = list(osis.utils.find_rootobject_types(model_path))
    
        for type_ in types:
            name = type_.__name__
            if name in ROOTOBJECT_TYPES:
                raise RuntimeError('Duplicate root object type %s' % name)
            ROOTOBJECT_TYPES[name] = type_
    
        self._update_rootobject_accessors()


    def _update_rootobject_accessors(self):
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
            if attr and isinstance(attr, RootPyModelObjectAccessor):
                logger.debug('Removing old type %s' % attrname)
                delattr(OsisConnection, attrname)
    
        # Now add all of them again
        for type_ in types.itervalues():
            name = getattr(type_, 'OSIS_TYPE_NAME', type_.__name__.lower())
            accessor = RootPyModelObjectAccessor(name, type_)
            logger.debug('Adding new type %s' % name)
            setattr(OsisConnection, name, accessor)
            
    def importDomain(self, domainname, specpath):
        self._initFromPath(specpath)
                
        try:
            self.__connection = OsisConnection(XMLRPCTransport('http://localhost:8888', 'osis_service'), ThriftSerializer)
        except:
            q.logger.log("[DRPClient] Failed to initialize the OSIS application server service connection: the DRPClient won't work...", 1)
            return
        
        try:
            self.__conn = OsisDB().getConnection('main')
        except:
             q.logger.log("[DRPClient] Failed to initialize the database connection for OSIS: the DRPClient won't work...", 1)
             return
        
        domain = Domain()
            
        from osis import ROOTOBJECT_TYPES as types
        for type in types.itervalues():
            name = getattr(type, 'OSIS_TYPE_NAME', type.__name__.lower())                
            #setattr(self, name, getattr(self.__connection, name))
            setattr(domain, name, getattr(self.__connection, name))
        setattr(self, domainname, domain)

                    
    def __initialize(self):
        
        #self._initFromPath(q.system.fs.joinPaths(q.dirs.baseDir, 'libexec','osis'))
        #self._initFromPath(q.system.fs.joinPaths(q.dirs.baseDir, 'lib', 'pymonkey', 'models'))
        parentPath = q.system.fs.joinPaths(q.dirs.baseDir, 'lib', 'pymonkey', 'models')
        for subPath in os.listdir(parentPath):
            domainname = subPath
            specpath = q.system.fs.joinPaths(parentPath, subPath)
            self.importDomain(domainname, specpath)
            