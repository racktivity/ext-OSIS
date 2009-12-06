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

import uuid
import datetime

class PG8000ConnectionResult(object):
    def __init__(self,desc,r):
        self.desc=desc
        self.r=r
    def getresult(self):
        return self.r
    def dictresult(self):
        
        def pgConvert(v):
            
            # Return same output a pymonkey DBConnection
            if v.__class__ == datetime.datetime:
                v = v.isoformat().replace('T', ' ')
            return v
            
        result=[dict([(self.desc[j][0], pgConvert(i[j])) for j in range(len(self.desc))]) for i in self.r]
        
        return result
    
def pg8000_uuid_in(s,**kwargs):
    return str(uuid.UUID(bytes=s))

class PG8000Connection(object):
    def __init__(self,ip,db,login,passwd):
        from pg8000 import DBAPI
        import pg8000.types
        # pg8000 doesn't support uuid
        pg8000.types.pg_types[2950]={"bin_in": pg8000_uuid_in}
        # convert unknown type to string
        pg8000.types.pg_types[705] ={"bin_in": pg8000.types.varcharin} # TEXT type
        self.pg8conn = DBAPI.connect(user=login, host=ip, database=db, password=passwd)
        
    def sqlexecute(self,*l):
        
        # PG8000 does noet support %
        l = (q.replace('%', '%%') for q in l)
        
        # Ugly part I
        t = [v for v in l]
        l = (v for v in t)
    
        cursor=self.pg8conn.cursor()
        cursor.execute(*l)
        desc=cursor.description
        
        # Check of we have a statement which returns a dataset
        # @todo: How can we improve this?
        # Ugly part II
        has_result = bool([True for v in t if v.strip().lower().startswith('select')])
        
        l = []
        
        if has_result:
            
            l=[i for i in cursor]
            
        self.pg8conn.commit()
            
        return PG8000ConnectionResult(desc,l)
