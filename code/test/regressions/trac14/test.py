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

'''Regression test for Trac ticket #14'''

import unittest
import os.path

from osis.test import init

from osis.client import OsisConnection
from osis.client.xmlrpc import XMLRPCTransport

class TestTrac14(unittest.TestCase):
    DOMAIN = "test_domain"
    def setUp(self):
        init(self.DOMAIN, os.path.dirname(__file__))

    def test_serialize(self):
        transport = XMLRPCTransport('http://localhost:8088')
        client = OsisConnection(transport, self.serializer)
        clientdomain = getattr(client, self.DOMAIN)
        comp = clientdomain.company.new(name='Aserver', url='http://www.aserver.com')

        employee1 = comp.employees.new(first_name='John', last_name='Doe')
        employee1.email_addresses.append('john.doe@aserver.com')
        employee1.email_addresses.append('john@aserver.com')
        comp.employees.append(employee1)

        serialized = comp.serialize(self.serializer)

        deserialized = comp.__class__.deserialize(self.serializer, serialized)
        self.assertEqual(deserialized.employees[0].email_addresses[0],
                         'john.doe@aserver.com')


import osis.test
osis.test.setup(globals())
