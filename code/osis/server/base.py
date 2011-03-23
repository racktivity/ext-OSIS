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

'''Base (abstract) implementation of the OSIS server interface'''

import os
import logging


from osis.server.exceptions import UnknownSerializerException, \
    UnknownObjectTypeException, ObjectNotFoundException
#TODO Move this to a more suitable place #pylint: disable-msg=W0511
from osis.store.OsisFilterObject import OsisFilterObject as Filter
from pylabs import q
from pymodel.serializers import SERIALIZERS
import pymodel

logger = logging.getLogger('osis.server.base') #pylint: disable-msg=C0103

#pylint: disable-msg=R0921
class BaseServer(object):
    '''Base implementation of the interface an OSIS server should expose

    This class handles the low-level stuff including serialization and
    deserialization of incoming and outgoing objects using the correct
    serializer, perform input validation and exception handling,...
    '''
    
    def __init__(self, model_paths=None, tasklet_path=None):
        '''Initialize the OSIS service

        @param model_paths: Paths where model definitions can be found
        @type model_paths: list of strings
        @param tasklet_path: Container path of OSIS tasklets
        @type tasklet_path: string
        '''
        tasklet_path = tasklet_path or \
                os.path.join(os.path.dirname(__file__), 'tasklets')
        self.tasklet_engine = q.taskletengine.get(tasklet_path)
        self.load_model_paths(model_paths)

    def _get(self, domain, object_type, guid, version, serializer):
        '''Helper method to retrieve a specific version of an object from the
        OSIS object store
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

        @return: Serialized object
        @rtype: string
        '''
        object_, serialized = self.get_object_from_store(domain, object_type, guid,
                                                         serializer)

        logger.debug('[GET] Object %s version %s type %s found' % \
                     (guid, version, object_type))

        if not serialized:
            try:
                serializer = SERIALIZERS[serializer]
            except KeyError:
                raise UnknownSerializerException(
                    'Unknown serializer type %s' % serializer)

            serialized = object_.serialize(serializer)

        return serialized


    def get(self, domain, object_type, guid, serializer):
        '''Retrieve an object from the OSIS object store
        @param domain: Domain of the object
        @type domain: string
        @param object_type: Object type name
        @type object_type: string
        @param guid: GUID of the object to retrieve
        @type guid: string
        @param serializer: Name of the serializer to use
        @type serializer: string

        @return: Serialized object
        @rtype: string
        '''
        logger.info('[GET] object_type=%s, guid=%s, serializer=%s' % \
                    (object_type, guid, serializer))

        return self._get(domain, object_type, guid, None, serializer)

    def get_version(self, domain, object_type, guid, version, serializer):
        '''Retrieve an object from the OSIS object store
        @param domain: Domain of the object
        @type domain: string
        @param object_type: Object type name
        @type object_type: string
        @param guid: GUID of the object to retrieve
        @type guid: string
        @param version: Version of the object to retrieve
        @type version: string
        @param serializer: Name of the serializer to use
        @type serializer: string

        @return: Serialized object
        @rtype: string
        '''
        logger.info('[GET] object_type=%s, guid=%s, serializer=%s' % \
                    (object_type, guid, serializer))

        return self._get(domain, object_type, guid, version, serializer)

    def delete(self, domain, object_type, guid):
        '''Delete an object from the OSIS object store
        @param domain: Domain of the object
        @type domain: string
        @param object_type: Object type name
        @type object_type: string
        @param guid: GUID of the object to delete
        @type guid: string

        @return: True or False, according as the deletion succeeds or fails
        '''
        
        # Set up tasklet call parameters
        params = {
             'domain': domain,
             'rootobjectguid': guid,
             'rootobjecttype': object_type,
             'rootobjectversionguid': None
        }

        self.tasklet_engine.execute(params=params, tags=('osis', 'delete'))

        if not 'result' in params or not params['result']:
            return False

        return params['result']

    def put(self, domain, object_type, data, serializer):
        '''Save an object in the OSIS object store
        @param domain: Domain of the object
        @type domain: string
        @param object_type: Object type name
        @type object_type: string
        @param data: Serialized object
        @type data: string
        @param serializer: Name of the serializer to use
        @type serializer: string
        '''

        try:
            class_ = pymodel.ROOTOBJECT_TYPES[domain][object_type]
        except KeyError:
            raise UnknownObjectTypeException('Object type %s is not known' % \
                                            object_type)

        try:
            serializer = SERIALIZERS[serializer]
        except KeyError:
            raise UnknownSerializerException('Unknown serializer type %s' % \
                                             serializer)

        object_ = class_.deserialize(serializer, data)

        self.put_object_in_store(domain, object_type, object_)

    def find(self, domain, object_type, filters, view=None):
        '''Execute a find (query) operation on the store
        @param domain: Domain of the object
        @type domain: string
        @param object_type: Object type name
        @type object_type: string
        @param filters: List of query filters
        @type filters: list
        @param view: Optional name of view to return
        @type view: string

        @return: OSISList-formatted result table
        @rtype: list
        '''
        # Even if '' is passed, we want none
        view = view or None

        if object_type not in pymodel.ROOTOBJECT_TYPES[domain]:
            raise UnknownObjectTypeException('Unknown object type %s' % \
                                             object_type)

        if isinstance(filters,Filter):
            filter_=filters
        else:
            filter_ = Filter()
            filter_.filters = filters

        result = self.execute_filter(domain, object_type, filter_, view)

        if not result:
            logger.debug('[FIND] No results found')
            return []

        # Commenting this line temporarily because "result[1]" leads
        # to a crash if 'result' is a simple list of guids and contains
        # a single entry. Need to break this function into two, one
        # expecting a 'view' argument, and another not.
        #logger.debug('[FIND] %d results found' % len(result[1]))
        return result

    def findAsView(self, domain, object_type, filters, view):
        '''Execute a find (query) operation on the store
        @param domain: Domain of the object
        @type domain: string
        @param object_type: Object type name
        @type object_type: string
        @param filters: List of query filters
        @type filters: list
        @param view: name of view to return
        @type view: string
        '''
        if object_type not in pymodel.ROOTOBJECT_TYPES[domain]:
            raise UnknownObjectTypeException('Unknown object type %s' % \
                                             object_type)

        filter_ = Filter()
        filter_.filters = filters

        result = self.execute_filter_as_view(domain, object_type, filter_, view)

        return result


    # Abstract methods
    def get_object_from_store(self, domain, object_type, guid, preferred_serializer, version=None):
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
        # Set up tasklet call parameters
        params = {
            'domain': domain,   
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

    def put_object_in_store(self, domain, object_type, object_):
        '''Store an object in the store
        @param domain: Domain of the object
        @type domain: string
        @param object_type: Object type name
        @type object_type: string
        @param object_: The object to store
        @type object_: object
        '''
        
        # Reset baseversion to the current version
        object_._baseversion = object_.version
        
        # Execute store taslkets
        params = {
            'domain': domain,
            'rootobject': object_,
            'rootobjecttype': object_type,
        }

        self.tasklet_engine.execute(params=params, tags=('osis', 'store',))

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
        
        params = {
            'domain': domain,
            'rootobjecttype': object_type,
            'filterobject': filter_,
            'osisview': view,
        }

        self.tasklet_engine.execute(params=params, tags=('osis','findobject'))

        if not 'result' in params or not params['result']:
            return list()

        return params['result']


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

        params = {
            'domain': domain,
            'rootobjecttype': object_type,
            'filterobject': filter_,
            'osisview': view,
        }

        self.tasklet_engine.execute(params=params, tags=('osis','findasview'))

        if not 'result' in params or not params['result']:
            return list()

        return params['result']

    def runQuery(self, query):
        '''Run query from OSIS server

        @param query: Query to execute on OSIS server
        @type query: string

        @return: result of the query else raise error
        @type: List of rows. Each row shall be represented as a dictionary.
        '''
        
        # Set up tasklet call parameters
        params = {'query': query, }
        self.tasklet_engine.execute(params=params, tags=('osis', 'query'))
        if not 'result' in params or not params['result']:
            return list()

        return params['result']

    def load_model_paths(self, model_paths=None):
        if model_paths is None:
            return

        for model_path in model_paths:
            self.load_model_path(model_path)

    def load_model_path(self, model_path):
        domain_names = (d for d in os.listdir(model_path) if os.path.isdir(os.path.join(model_path, d)))
        for domain_name in domain_names:
            domain_path = os.path.join(model_path, domain_name)
            pymodel.init(domain_path, domain_name)
