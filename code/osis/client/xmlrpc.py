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

'''XMLRPC OSIS client transport implementation'''

import base64
import logging
import xmlrpclib

logger = logging.getLogger('osis.client.xmlrpc') #pylint: disable-msg=C0103

class XMLRPCTransport(object):
    '''XMLRPC transport to communicate with an XMLRPC OSIS server'''
    def __init__(self, uri, service_name=None):
        '''Initialize a new XMLRPC transport

        @param uri: URI of the XMLRPC server
        @type uri: string
        @param service_name: Name of the service endpoint (if applicable)
        @type service_name: string
        '''
        self.proxy = xmlrpclib.ServerProxy(uri,allow_none=True)

        if service_name:
            self.proxy = getattr(self.proxy, service_name)

    def get(self, object_type, guid, serializer):
        '''Retrieve an serialized object from the server

        @param guid: Root object GUID
        @type guid: string
        @param serializer: Name of the serialization method being used
        @type serializer: string

        @return: Serialized root object instance
        @rtype: string
        '''
        logger.debug('GET %s %s' % (object_type, guid))
        return base64.decodestring(self.proxy.get(object_type, guid, serializer))

    def get_version(self, object_type, guid, version, serializer):
        '''Retrieve an serialized object from the server

        @param guid: Root object GUID
        @type guid: string
        @param version: GUID of the object version to retrieve
        @type version: string
        @param serializer: Name of the serialization method being used
        @type serializer: string

        @return: Serialized root object instance
        @rtype: string
        '''
        logger.debug('GET %s %s version %s' % (object_type, guid, version))
        return base64.decodestring(self.proxy.get_version(object_type, guid,
            version, serializer))

    def runQuery(self, query, *args, **kwargs):
        '''Run query from OSIS server

        @param query: Query to execute on OSIS server
        @type query: string

        @return: result of the query else raise error
        @type: List of rows. Each row shall be represented as a dictionary.
        '''

        return self.proxy.runQuery(query, *args, **kwargs)

    def delete(self, object_type, guid):
        '''Delete a serialized object from the server

        @param guid: Root object GUID
        @type guid: string

        @return: True or False, according as the deletion succeeds or fails.
        '''
        logger.debug('DELETE %s %s' % (object_type, guid))
        return self.proxy.delete(object_type, guid)

    def delete_version(self, object_type, guid, version):
        '''Delete a serialized object from the server

        @param guid: Root object GUID
        @type guid: string
        @param version: GUID of the object version to delete
        @type version: string

        @return: True or False, according as the deletion succeeds or fails.
        '''
        logger.debug('DELETE %s %s %s version %s' % (object_type, guid, version))
        return self.proxy.delete_version(object_type, guid, version)


    def put(self, object_type, data, serializer):
        '''Store a serialized object to the server

        @param data: Serialized object data
        @type data: string
        @param serializer: Name of the serialization method being used
        @type serializer: string
        '''
        data = base64.encodestring(data)
        logger.debug('PUT %s' % (object_type, ))
        self.proxy.put(object_type, data, serializer)

    def find(self, object_type, filter_, view):
        '''Perform a filter operation on the server

        @param filter_: Filter definition
        @type filter_: L{OsisFilterObject}
        @param view: View to return
        @type view: string

        @return: List of GUIDs or OsisList of data
        @rtype: tuple<string> or tuple
        '''
        filter_data = filter_.filters

        if view:
            return self.proxy.find(object_type, filter_data, view)
        else:
            return self.proxy.find(object_type, filter_data)

    def findAsView(self, object_type, filter_, view):
        '''Perform a filter operation on the server

        @param filter_: Filter definition
        @type filter_: L{OsisFilterObject}
        @param view: View to return
        @type view: string

        @return: List of GUIDs or OsisList of data
        @rtype: list
        '''
        return self.proxy.findAsView(object_type, filter_.filters, view)
