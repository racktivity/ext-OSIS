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

import re

from pymonkey import q
from pymonkey.baseclasses.BaseEnumeration import BaseEnumeration, EnumerationWithValue

class OsisView(object):

    def __init__(self, domain, objType, name):
        self.domain = domain
        self.name = name;
        self.objType = objType;
        self.columns = {}
        self.setCol('viewguid', q.enumerators.OsisType.UUID, False)
        self.setCol('guid', q.enumerators.OsisType.UUID, False)
        self.schema = '%s_%s' % (self.domain, self.objType)
        

    def setCol(self, name, datatype, nullable):
        if not self.columns.has_key(name):
            self.columns[name] = OsisColumn(name, datatype, nullable);


    def buildSql(self):
        
        
        fields = []
        for col in self.columns.itervalues():
            fields.append(col.sqlString())
        fieldlist = '\n'.join(fields)[1:]
        sql = list()
        sql.append("CREATE TABLE %s.%s (%s)  WITH (OIDS=FALSE) ;"%(self.schema, self.name, fieldlist))
        sql.append("CREATE INDEX guid_%(objType)s_%(name)s ON %(schema)s.%(name)s (guid)"%{'objType':self.objType, 'name':self.name, 'schema': self.schema})
        return sql


class OsisColumn(object):
    def __init__(self, name, datatype, nullable):
        self.name = name
        self.datatype = datatype
        self.nullable = nullable

    def sqlString(self):
        if not self.nullable:
            return ",\"%s\"  %s NOT NULL"%(self.name, self.datatype.value)
        else:
            return ",\"%s\"  %s"%(self.name, self.datatype.value)


class OsisType(EnumerationWithValue):
    pass

OsisType.registerItem("integer", "integer")
OsisType.registerItem("bigint", "bigint")
OsisType.registerItem("string", "character varying(1024)")
OsisType.registerItem("text", "text")
OsisType.registerItem("uuid", "uuid")
OsisType.registerItem("datetime", "timestamp without time zone")
OsisType.registerItem("boolean", "boolean")
OsisType.registerItem("binary", "bytea[]")
OsisType.finishItemRegistration()