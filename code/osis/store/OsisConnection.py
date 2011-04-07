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
from pylabs.baseclasses import BaseEnumeration
from pylabs.db.DBConnection import DBConnection
from OsisView import OsisView
from OsisFilterObject import OsisFilterObject

from pg import ProgrammingError
import exceptions
import traceback

import sqlalchemy

def get_table_name(domain, objType):
    return "%s_view_%s_list" % (domain, objType)

class QueryValue(BaseEnumeration):
    """Utility class which gives string representation of Log Type """

    def __init__(self, level):
        self.level = level

    def __int__(self):
        return self.level

    def __repr__(self):
        return str(self)

QueryValue.registerItem('None', 0)
QueryValue.finishItemRegistration()

class OsisException(exceptions.Exception):
    def __init__(self, command, msg):
        msg = self.handleException(command, msg)
        self.errmsg = msg
        self.args = (msg,)

    def handleException(self, command, msg):
        errorMsg = 'Exception occurred while executing \"%s\".\n'%command
        errorMsg += traceback.format_exc()
        return errorMsg

class _OsisPGTypeConverter(object):
    def __init__(self):
        self._pgType2pyType = {}
        self._pgType2pyType["integer"] = "int"
        self._pgType2pyType["character varying"] = "str"
        self._pgType2pyType["text"] = "str"
        self._pgType2pyType["timestamp without time zone"] = "datetime"
        self._pgType2pyType["ARRAY"] = "hex"
        self.requiresConvert = ['boolean', 'bool']

    def convertType(self, pgType):
        if not pgType in ('bool', 'str', 'datetime', 'date', 'int', 'uuid'):
            return self._pgType2pyType[pgType]
        return pgType

    def convertValue(self, pgType, pgValue):
        if pgValue == None: return ""
        if pgType in  ('boolean', 'bool'):
            if pgValue.__class__ == bool:
                return pgValue
            if 'f' in pgValue:
                return False
            elif 't' in pgValue:
                return True
        return pgValue

osisPGTypeConverter = _OsisPGTypeConverter()


class OsisConnectionGeneric(object):
    def __init__(self):
        self._dbConn = None
        self._login = None

        self._sqlalchemy_engine = None
        self._sqlalchemy_metadata = None

    def connect(self, ip, db, login, passwd):
        """
        Connect to the postgresql server

        @param ip : ip of the db server
        @param db : database to connect to
        @param login : login to connect
        @param passwd : password to connect
        """
        raise Exception("unimplemented generic connect")

    def runQuery(self, query):
        '''Run query from OSIS server

        @param query: Query to execute on OSIS server
        @type query: string

        @return: result of the query else raise error
        @type: List of rows. Each row shall be represented as a dictionary.
        '''
        try:
            return self.__executeQuery(query)
        except ProgrammingError,ex:
            raise OsisException(query, ex)

    def createObjectType(self, domain, objType):
        """
        Creates the model structure on the database

        @param domain : domain to create the object in
        @param objType : the object type to create
        """
        objTypeName = objType.__class__.__name__
        self.createObjectTypeByName(domain, objTypeName)
        
    def createObjectTypeByName(self, domain,  objTypeName):
        '''
        @param domain : domain to create the object in
        @param objTypeName : name of the object type to create
        '''
        if self.schemeExists(domain, objTypeName):
            q.logger.log("ObjectType %s already exists"%objTypeName ,3)
            return
        self.schemeCreate(domain, objTypeName)

    def schemeCreate(self, domain, name):
        """
        Creates the model structure on the database

        @param domain : domain to create the scheme in
        @param objTypeName : the name of the type to create
        """
        if self.schemeExists(domain, name):
            q.logger.log("Schema %s already exists in domain %s" % (name, domain) ,3)
            return

        schema = self._getSchemeName(domain, name)
        
        sqls = ['CREATE SCHEMA %s' % schema]
        
        for sql in sqls:
            self.__executeQuery(sql, False)

    def schemeExists(self, domain, name):
        """
        Checks if the schema with the supplied name exists

        @param domain : domain to check for the schema
        @param name : name of the schema to check
        """
        schema = self._getSchemeName(domain, name)
        
        sql =  "select distinct schemaname as name from pg_tables where schemaname = '%s'" % schema
        result = self.__executeQuery(sql)
        
        if result:
            return True
        else:
            return False
        
    def _getSchemeName(self, domain, name):
        return '%s_%s' % (domain, name)

    def viewExists(self, domain, objType, viewname):
        """
        Checks if the requested view exists in the supplied schema

        @param domain : domain where the view lives 
        @param objType : the object type to check
        @param viewname : name of the view to check
        """
        
        if not self.schemeExists(domain, objType):
            return False
        
        schema = self._getSchemeName(domain, objType)
        
        sql =  "select distinct schemaname, tablename from pg_tables where schemaname = '%s' and tablename = '%s'"%(schema, viewname)
        result = self.__executeQuery(sql)
        if result:
            return True
        else:
            return False

    def _find_table(self, schema, name):
        try:
            full_name = '%s.%s' % (schema, name)
            return self._sqlalchemy_metadata.tables[full_name]
        except KeyError:
            pass

        self._sqlalchemy_metadata.reflect(
            bind=self._sqlalchemy_engine, schema=schema, only=(name, ))

        return self._sqlalchemy_metadata.tables[full_name]

    def objectsFind(self, domain, objType, filterobject, viewToReturn=None):
        """
        returns a list of matching guids according to the supplied fitlerobject filters

        @param domain : domain where the objects live
        @param objType : type of object to search
        @param filterobject : a list of filters indicating the view and field-value to use to filter
        @param viewToReturn : the view to use to return the list of found objects
        """
        schema = self._getSchemeName(domain, objType)
        if viewToReturn:
            table_name = viewToReturn
        else:
            table_name = get_table_name(domain, objType)

        # Step 1: turn the filters into a more sane datastructure
        filters = set()
        for filter_ in filterobject.filters:
            view = filter_.keys()[0]
            field = filter_[view].keys()[0]
            value, exact = filter_[view][field]

            filters.add((view, field, value, exact, ))

        filters = tuple(filters)

        # Step 2: Create list of values to retrieve
        table = self._find_table(schema, table_name)
        fields = []
        for c in table.c:
            # Convert datetime fields to str for backwards compatibility
            if isinstance(c.type, (sqlalchemy.types.DATETIME,
                              sqlalchemy.types.TIMESTAMP,
                              sqlalchemy.types.DATE,
                              sqlalchemy.types.TIME,)):
                fields.append(sqlalchemy.sql.cast(c, sqlalchemy.types.VARCHAR))
            else:
                fields.append(c)

        # TODO Column type names?! I don't get why we need this anyway
        coldefs = tuple((c.name, 'string') for c in table.c)

        # Step 3: Set up joins
        from_obj = reduce(
            lambda f, t: f.join(t, t.c.guid == table.c.guid),
            set(self._find_table(schema, filter_[0]) for filter_ in filters if filter_[0] != table_name),
            table)

        # Step 4: Create 'where' clause
        def create_clause((view, field,value, exact, )):
            table = self._find_table(schema, view)
            col = table.c[field]

            if isinstance(col.type,
                (sqlalchemy.types.VARCHAR, sqlalchemy.types.NVARCHAR,)) and not exact:
                return (col.like('%%%s%%' % value))
            else:
                return (col == value)

        if filters:
            base = create_clause(filters[0])
            where_clause = reduce(lambda w, f: w & create_clause(f),
                filters[1:], base)
        else:
            where_clause = None

        # Step 4: Set up basic select query
        query = sqlalchemy.sql.select(fields, where_clause, from_obj=from_obj)

        # Step 5: Execute query and return result
        result = None
        try:
            result = self._sqlalchemy_engine.execute(query)

            if not viewToReturn:
                return tuple(row['guid'] for row in result)
            else:
                rows = tuple(tuple(row.values()) for row in result)
                return coldefs, rows

        finally:
            if result:
                result.close()

    def objectsFindAsView(self, domain,  objType, filterObject, viewName):
        """
        Find
        
        @param domain : the object Type's domain 
        @param objType : type of object to search
        @param filterobject : a list of filters indicating the view and field-value to use to filter
        @param viewToReturn : the view to use to return the list of found objects
        """
        cols, rows = self.objectsFind(domain, objType, filterObject, viewName)

        return tuple(
            dict((col[0], row[i]) for (i, col) in enumerate(cols)) for row in rows)


    def getFilterObject(self):
        """
        returns an object to hold the filter criteria
        """
        return OsisFilterObject()

    def viewCreate(self, domain, objType, viewName):
        """
        Creates and returns a new view object

        @param domain : the object Type's domain 
        @param objType : the object type on which to add the view
        @param viewName : the name of the view
        """

        if not self.schemeExists(domain, objType):
            self.schemeCreate(domain, objType)

        if not self.viewExists(domain, objType, viewName):
            return OsisView(domain, objType, viewName)
        else:
            q.eventhandler.raiseCriticalError('[%s] already has a view [%s].'%(objType, viewName))

    def viewAdd(self, view):
        """
        Adds the new view to the database

        @param view : Osisview object to create on the database
        """
        for sql in view.buildSql():
            self.__executeQuery(sql, False)


    def viewDestroy(self, domain, objType, viewName):
        """
        Removes a view from the database
        
        @param domain : the object Type's domain 
        @param objType : the type of object to destroy
        @param viewName : Osisview object to destroy
        """
        schema = self._getSchemeName(domain, objType)
        
        if not self.viewExists(domain, objType, viewName):
            q.eventhandler.raiseCriticalError('%s.%s not found.'%(schema, viewName))
            return

        sql = 'DROP TABLE %s.%s CASCADE'%(schema, viewName)
        self.__executeQuery(sql, False)
        return True

    def viewDelete(self, domain, objType, viewName, guid, versionguid=None):
        """
        Removes row(s) with the supplied guid from the view

        @param domain : the object Type's domain  
        @param objType : the object Type name
        @param viewName : the view from which to remove a row
        @param viewguid : unique identifier (GUID) for the object
        @param versionguid : unique identifier indicating the version of the object. (OBSOLETED)
                             If specified, only the mentioned version will be removed,
                             If ommited, all versions will be removed !
        """

        schema = self._getSchemeName(domain, objType)
        
        sql = "delete from %s.%s where guid='%s'" % (schema, viewName, guid)
        
        self.__executeQuery(sql, False)
        return True


    def viewSave(self, domain, objType, viewName, guid, versionguid, fields):
        """
        Add a new row to the view

        @param domain : the object Type's domain 
        @param objType : the object Type name
        @param viewName : the view from which to remove a row
        @param guid : unique identifier for the object
        @param versionguid : unique identifier indicating the version of the object (OBSOLETED)
        @param fields : dict containing the field:values
        """
        # Remove current entry (if any)
        self.viewDelete(domain, objType, viewName, guid, versionguid)

        # Prepare values
        newViewGuid = q.base.idgenerator.generateGUID()
        if not isinstance(fields, list):
            fields = [fields,]

        schema = self._getSchemeName(domain, objType)

        # Add new entry
        table = self._find_table(schema, viewName)

        for field in fields:
            # Add missing field data
            field.update({
                'guid': guid,
                'viewguid': newViewGuid,
            })

            for k, v in field.iteritems():
                if isinstance(v, BaseEnumeration):
                    field[k] = str(v)

            query = table.insert().values(values=field)

            result = None
            try:
                result = self._sqlalchemy_engine.execute(query, field)
            finally:
                if result:
                    result.close()

    def __executeQuery(self, query, getdict= True):
        query = self._dbConn.sqlexecute(query)
        if getdict and query:
            return query.dictresult() if hasattr(query, 'dictresult') else dict()

_SA_ENGINES = dict()

class OsisConnectionPYmonkeyDBConnection(OsisConnectionGeneric):
    def connect(self, ip, db, login, passwd):
        self._dbConn = DBConnection(ip, db, login, passwd)
        self._login = login

        dsn = 'postgresql://%(user)s:%(password)s@%(host)s/%(db)s' % {
            'host': ip,
            'user': login,
            'password': passwd,
            'db': db,
        }

        if dsn in _SA_ENGINES:
            self._sqlalchemy_engine = _SA_ENGINES[dsn]
        else:
            _SA_ENGINES[dsn] = sqlalchemy.create_engine(dsn)
            self._sqlalchemy_engine = _SA_ENGINES[dsn]

        self._sqlalchemy_metadata = sqlalchemy.MetaData()

        return dict()

class OsisConnectionPG8000(OsisConnectionGeneric):
    def connect(self, ip, db, login, passwd):
        from PG8000Connection import PG8000Connection
        self._dbConn = PG8000Connection(ip, db, login, passwd)
        self._login = login

def OsisConnection(usePG8000=False):
    # If stackless uses pg8000
    if usePG8000:
        return OsisConnectionPG8000()
    else:
        return OsisConnectionPYmonkeyDBConnection()
    # else uses PYmonkeyDBConnection one
    #return OsisConnectionPYmonkeyDBConnection()
