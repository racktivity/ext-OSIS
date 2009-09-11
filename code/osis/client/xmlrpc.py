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

    def get(self, type_, guid, serializer):
        '''Retrieve an serialized object from the server

        @param type_: Root object type name
        @type type_: string
        @param guid: Root object GUID
        @type guid: string
        @param serializer: Name of the serialization method being used
        @type serializer: string

        @return: Serialized root object instance
        @rtype: string
        '''
        logger.debug('GET %s %s' % (type_, guid))
        return base64.decodestring(self.proxy.get(type_, guid, serializer))

    def get_version(self, type_, guid, version, serializer):
        '''Retrieve an serialized object from the server

        @param type_: Root object type name
        @type type_: string
        @param guid: Root object GUID
        @type guid: string
        @param version: GUID of the object version to retrieve
        @type version: string
        @param serializer: Name of the serialization method being used
        @type serializer: string

        @return: Serialized root object instance
        @rtype: string
        '''
        logger.debug('GET %s %s version %s' % (type_, guid, version))
        return base64.decodestring(self.proxy.get_version(type_, guid,
                                                          version, serializer))

    def runQuery(self,query):
        '''Run query from OSIS server

        @param query: Query to execute on OSIS server
        @type query: string

        @return: result of the query else raise error
        @type: List of rows. Each row shall be represented as a dictionary.
        '''

	return self.proxy.runQuery(query)

    def delete(self, type_, guid):
        '''Delete a serialized object from the server

        @param type_: Root object type name
        @type type_: string
        @param guid: Root object GUID
        @type guid: string

        @return: True or False, according as the deletion succeeds or fails.
        '''
        logger.debug('DELETE %s %s' % (type_, guid))
        return self.proxy.delete(type_, guid)

    def delete_version(self, type_, guid, version):
        '''Delete a serialized object from the server

        @param type_: Root object type name
        @type type_: string
        @param guid: Root object GUID
        @type guid: string
        @param version: GUID of the object version to delete
        @type version: string

        @return: True or False, according as the deletion succeeds or fails.
        '''
        logger.debug('DELETE %s %s version %s' % (type_, guid, version))
        return self.proxy.delete_version(type_, guid, version)


    def put(self, type_, data, serializer):
        '''Store a serialized object to the server

        @param type_: Root object type name
        @type type_: string
        @param data: Serialized object data
        @type data: string
        @param serializer: Name of the serialization method being used
        @type serializer: string
        '''
        data = base64.encodestring(data)
        logger.debug('PUT %s' % type_)
        self.proxy.put(type_, data, serializer)

    def find(self, type_, filter_, view):
        '''Perform a filter operation on the server

        @param type_: Root object type name
        @type type_: string
        @param filter_: Filter definition
        @type filter_: L{OsisFilterObject}
        @param view: View to return
        @type view: string

        @return: List of GUIDs or OsisList of data
        @rtype: tuple<string> or tuple
        '''
        filter_data = filter_.filters

        if view:
            return self.proxy.find(type_, filter_data, view)
        else:
            return self.proxy.find(type_, filter_data)

    def findAsView(self, type_, filter_, view):
        '''Perform a filter operation on the server

        @param type_: Root object type name
        @type type_: string
        @param filter_: Filter definition
        @type filter_: L{OsisFilterObject}
        @param view: View to return
        @type view: string

        @return: List of GUIDs or OsisList of data
        @rtype: list
        '''
        filter_data = filter_.filters

	return self.proxy.findAsView(type_, filter_data, view)
