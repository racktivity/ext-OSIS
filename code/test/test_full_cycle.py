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

import sys
import os.path
import base64
import unittest

from osis.server.base import BaseServer

def cleanup_environment():
    from osis import ROOTOBJECT_TYPES

    ROOTOBJECT_TYPES.clear()
    for modulename in sys.modules.keys():
        if modulename.startswith('osis._rootobjects'):
            sys.modules.pop(modulename)

    from osis.client.connection import update_rootobject_accessors
    update_rootobject_accessors()


class FakeXMLRPCServer(BaseServer):
    def __init__(self):
        self.data = dict()

    def get(self, type_, guid, serializer):
        data = BaseServer.get(self, type_, guid, serializer)
        return base64.encodestring(data)

    def get_version(self, type_, guid, version, serializer):
        data = BaseServer.get_version(self, type_, guid, version, serializer)
        return base64.encodestring(data)

    def put(self, type_, data, serializer):
        data = base64.decodestring(data)
        BaseServer.put(self, type_, data, serializer)
        return True

    def get_object_from_store(self, object_type, guid, preferred_serializer,
                              version=None):
        version = version or 'latest'

        if not object_type in self.data:
            raise ObjectNotFoundException

        if not guid in self.data[object_type]:
            raise ObjectNotFoundException

        if version and version not in self.data[object_type][guid]:
            raise ObjectNotFoundException

        return self.data[object_type][guid][version], None

    def put_object_in_store(self, object_type, object_):
        if not object_type in self.data:
            self.data[object_type] = dict()

        if not object_.guid in self.data[object_type]:
            self.data[object_type][object_.guid] = dict()

        self.data[object_type][object_.guid][object_.version] = object_
        self.data[object_type][object_.guid]['latest'] = object_

    def execute_filter(self, object_type, filter_, view):
        raise NotImplementedError

server = FakeXMLRPCServer()


class FakeXMLRPCTransport(object):
    def __init__(self, uri, service_name=None):
        pass

    def get(self, type_, guid, serializer):
        data = server.get(type_, guid, serializer)
        return base64.decodestring(data)

    def get_version(self, type_, guid, version, serializer):
        data = server.get_version(type_, guid, version, serializer)
        return base64.decodestring(data)

    def put(self, type_, data, serializer):
        data = base64.encodestring(data)
        return server.put(type_, data, serializer)

    def find(self, type_, filter_, view):
        return server.find(type_, filter_, view)


class TestFullCycle(unittest.TestCase):
    def patch_xmlrpc_transport(self):
        import osis.client.xmlrpc
        self._original_xmlrpc_transport = osis.client.xmlrpc.XMLRPCTransport
        osis.client.xmlrpc.XMLRPCTransport = FakeXMLRPCTransport

    def unpatch_xmlrpc_transport(self):
        import osis.client.xmlrpc
        osis.client.xmlrpc.XMLRPCTransport = self._original_xmlrpc_transport

    def setUp(self):
        cleanup_environment()
        self.patch_xmlrpc_transport()

    def tearDown(self):
        cleanup_environment()
        self.unpatch_xmlrpc_transport()

    def test_0010_initialize_osis(self):
        '''Initialize the OSIS system'''
        from osis import init
        model_path = os.path.abspath(
                        os.path.join(os.path.dirname(__file__), '_models'))
        init(model_path)

    def test_0020_instanciate_transport(self):
        '''Instanciate an XMLRPC transport'''
        self.test_0010_initialize_osis()
        from osis.client.xmlrpc import XMLRPCTransport
        self.transport = XMLRPCTransport('http://localhost:8000', 'osis')

    def test_0030_instanciate_connection(self):
        '''Instanciate an OSIS connection'''
        self.test_0020_instanciate_transport()
        from osis.client import OsisConnection
        self.connection = OsisConnection(self.transport, self.serializer)

    def test_0040_create_object_instance(self):
        '''Create a simple object'''
        self.test_0030_instanciate_connection()
        self.object_ = self.connection.simple.new()

    def test_0050_set_object_data(self):
        '''Set simple object data'''
        self.test_0040_create_object_instance()
        self.object_.i = 123

    def test_0060_save_object(self):
        '''Save simple object'''
        self.test_0050_set_object_data()
        self.connection.simple.save(self.object_)

    def test_0070_retrieve_object(self):
        '''Retrieve simple object'''
        self.test_0060_save_object()
        guid = self.object_.guid

        self.object2 = self.connection.simple.get(guid)

    def test_0080_compare_objects(self):
        '''Compare stored and retrieved object'''
        self.test_0070_retrieve_object()
        self.assert_(self.object_ is not self.object2)
        self.assertEquals(self.object_.i, self.object2.i)

    def test_0090_retrieve_object_version(self):
        '''Retrieve object version'''
        self.test_0080_compare_objects()
        guid = self.object_.guid
        version = self.object_.version

        self.object3 = self.connection.simple.get(guid, version)

    def test_0100_compare_objects(self):
        '''Compare stored and retrieved object'''
        self.test_0090_retrieve_object_version()
        self.assert_(self.object_ is not self.object3)
        self.assertEquals(self.object_.i, self.object3.i)


import osis.test
osis.test.setup(globals())
