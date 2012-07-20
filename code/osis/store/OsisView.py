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

from pylabs import q
from pylabs.baseclasses.BaseEnumeration import EnumerationWithValue

import sqlalchemy

class OsisView(object):
    def __init__(self, domain, objType, name, scheme):
        self.domain = domain
        self.name = name
        self.objType = objType
        self.schema = scheme
        self.columns = {}
        self.setCol('viewguid', q.enumerators.OsisType.UUID, False)
        self.setCol('guid', q.enumerators.OsisType.UUID, False, index=True)

    def setCol(self, name, datatype, nullable, index=False, unique=False):
        self.columns[name] = OsisColumn(name, datatype, nullable, index, unique)

    def buildTable(self, metadata):
        table = sqlalchemy.Table(self.name, metadata, schema=self.schema)

        for col in self.columns.itervalues():
            table.append_column(sqlalchemy.Column(col.name, col.datatype.value, nullable=col.nullable))

            if col.index:
                #add index
                sqlalchemy.Index("%s_%s" % (self.name, col.name), getattr(table.c, col.name), unique=col.unique)

        return table


class OsisColumn(object):
    def __init__(self, name, datatype, nullable, index=False, unique=False):
        self.name = name
        self.datatype = datatype
        self.nullable = nullable
        self.index = index
        self.unique = unique

class OsisType(EnumerationWithValue):
    pass

OsisType.registerItem("integer", sqlalchemy.Integer()) #pylint: disable=E1101
OsisType.registerItem("bigint", sqlalchemy.BigInteger()) #pylint: disable=E1101
OsisType.registerItem("float", sqlalchemy.Float()) #pylint: disable=E1101
OsisType.registerItem("string", sqlalchemy.String(1024)) #pylint: disable=E1101
OsisType.registerItem("text", sqlalchemy.Text()) #pylint: disable=E1101
OsisType.registerItem("uuid", sqlalchemy.String(46)) #pylint: disable=E1101
OsisType.registerItem("datetime", sqlalchemy.DateTime()) #pylint: disable=E1101
OsisType.registerItem("boolean", sqlalchemy.Boolean()) #pylint: disable=E1101
OsisType.registerItem("binary", sqlalchemy.LargeBinary()) #pylint: disable=E1101
OsisType.finishItemRegistration() #pylint: disable=E1101
