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

import logging

from osis.server.exceptions import UnknownSerializerException, \
    UnknownObjectTypeException
from osis.model.serializers import SERIALIZERS
from osis import ROOTOBJECT_TYPES
#TODO Move this to a more suitable place #pylint: disable-msg=W0511
from osis.store.OsisFilterObject import OsisFilterObject as Filter

logger = logging.getLogger('osis.server.base') #pylint: disable-msg=C0103

#pylint: disable-msg=R0921
class BaseServer(object):
    '''Base implementation of the interface an OSIS server should expose

    This class handles the low-level stuff including serialization and
    deserialization of incoming and outgoing objects using the correct
    serializer, perform input validation and exception handling,...
    '''
    def _get(self, object_type, guid, version, serializer):
        '''Helper method to retrieve a specific version of an object from the
        OSIS object store

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
        object_, serialized = self.get_object_from_store(object_type, guid,
                                                         serializer, version)

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


    def get(self, object_type, guid, serializer):
        '''Retrieve an object from the OSIS object store

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

        return self._get(object_type, guid, None, serializer)

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

        @return: Serialized object
        @rtype: string
        '''
        logger.info('[GET] object_type=%s, guid=%s, version=%s, '
                    'serializer=%s' % (object_type, guid, version, serializer))

        return self._get(object_type, guid, version, serializer)


    def put(self, object_type, data, serializer):
        '''Save an object in the OSIS object store

        @param object_type: Object type name
        @type object_type: string
        @param data: Serialized object
        @type data: string
        @param serializer: Name of the serializer to use
        @type serializer: string
        '''
        logger.info('[PUT] object_type=%s, serializer=%s' % \
                    (object_type, serializer))

        try:
            class_ = ROOTOBJECT_TYPES[object_type]
        except KeyError:
            raise UnknownObjectTypeException('Object type %s is not known' % \
                                            object_type)

        try:
            serializer = SERIALIZERS[serializer]
        except KeyError:
            raise UnknownSerializerException('Unknown serializer type %s' % \
                                             serializer)

        object_ = class_.deserialize(serializer, data)

        self.put_object_in_store(object_type, object_)

        logger.debug('[PUT] Object %s %s stored' % \
                     (object_type, object_.guid))

    def find(self, object_type, filters, view=None):
        '''Execute a find (query) operation on the store

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

        logger.info('[FIND] object_type=%s, filters=%s, view=%s' % \
                    (object_type, repr(filters), str(view)))

        if object_type not in ROOTOBJECT_TYPES:
            raise UnknownObjectTypeException('Unknown object type %s' % \
                                             object_type)

        filter_ = Filter()
        filter_.filters = filters

        result = self.execute_filter(object_type, filter_, view)

        if not result:
            logger.debug('[FIND] No results found')
            return (tuple(), tuple())

        logger.debug('[FIND] %d results found' % len(result[1]))
        return result

    # Abstract methods
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
        raise NotImplementedError

    def put_object_in_store(self, object_type, object_):
        '''Store an object in the store

        @param object_type: Object type name
        @type object_type: string
        @param object_: The object to store
        @type object_: object
        '''
        raise NotImplementedError

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
        raise NotImplementedError
