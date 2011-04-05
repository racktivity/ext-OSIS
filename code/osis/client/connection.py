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

# This is a rather poor implementation
# But at this moment I don't care since everything is a single ton anyway
class _Client(object):
    pass

class _Shelve(object):
    pass


class _Accessor(object):
    def __init__(self, model_type, model, transport, serializer):
        self.transport = transport
        self._ROOTOBJECTTYPE = model
        self.serializer = serializer

        self.object_type = model_type

    def get(self, guid, version=None):
        '''Retrieve a root object with a given GUID from the OSIS server

        If no version is specified, the latest version is retrieved.

        @param guid: GUID of the root object to retrieve
        @type guid: string

        @return: Root object instance
        @rtype: L{osis.model.RootObjectModel}
        '''
        #pylint: disable-msg=E1101
        if not version:
            data = self.transport.get(self.object_type, guid,
                self.serializer.NAME)
        else:
            data = self.transport.get_version(self.object_type, guid, version,
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
        return self.transport.delete(self.object_type, guid)

    def save(self, object_):
        '''Save a root object to the server

        @param object_: Object to store
        @type object_: L{osis.model.RootObjectModel}
        '''
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

        result = self.transport.put(self.object_type, data, self.serializer.NAME)

        # If everything is ok, set baseversion to version 
        object_._baseversion = object_.version

        return result

    def new(self, *args, **kwargs): #pylint: disable-msg=W0142
        '''Create a new instance of the root object type

        All arguments are handled verbatim to the root object type constructor.
        '''
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
        result = self.transport.find(self.object_type, filter_, view)

        return ViewResultList(result) if view else result

    def findAsView(self, filter_, viewName):
        """
        Perform a find/filter operation.
        @param filter_: Filter description
        @type filter_: OsisFilterObject
        @param view: name of the view to return
        @type view: string

        @return: list of dicts representing the view{col: value}
        """
        return self.transport.findAsView(self.object_type, filter_, viewName)

def generate_client(models, transport, serializer):
    client = _Client()

    for model_type, model in models:
        current = client
        model_type = tuple(model_type)

        if len(model_type) > 2:
            for part in model_type[1:-1]:
                if hasattr(current, part):
                    current = getattr(current, part)
                else:
                    current_ = _Shelve()
                    setattr(current, part, current_)
                    current = current_

                assert isinstance(current, _Shelve)

        accessor = _Accessor(model_type, model, transport, serializer)
        setattr(current, model_type[-1], accessor)

    return client
