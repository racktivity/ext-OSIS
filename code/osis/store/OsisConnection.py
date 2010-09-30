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
import datetime, time

from pymonkey import q
from pymonkey.baseclasses.ManagementApplication import ManagementApplication
from pymonkey.baseclasses import BaseEnumeration
from pymonkey.db.DBConnection import DBConnection
from OsisView import OsisView, OsisColumn, OsisType
from OsisFilterObject import OsisFilterObject

import sqlalchemy
import sqlalchemy.sql
import sqlalchemy.types

from osis.model.serializers import ThriftSerializer
from pg import ProgrammingError
import exceptions
import traceback
import uuid

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
        pyType = self.convertType(pgType)
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


    def objectExists(self, objType, guid, version):
        """
        Checks if an instance of objType with the supplied guid exists

        @param objType : type of object to check
        @param guid : unique identifier
        @param version : unique version for the given guid
        """

        return self.viewObjectExists(objType, 'main', guid, version)

    def viewObjectExists(self, objType, viewName, guid, version):
        """
        Checks if an instance of objType with the supplied guid exists

        @param objType : type of object to check
        @param viewName : view whixh contains the object
        @param guid : unique identifier
        @param version : unique version for the given guid
        """
        if not version:
	    sql = "select * from only %s.%s where guid='%s'"%(objType, viewName, guid)
        else:
	    sql ="select * from %s.%s where guid='%s' and version='%s'"%(objType, viewName, guid, version)

	result = self.__executeQuery(sql)
        if result:
            return result[0] > 0
        return False


    def objectGet(self, objType,guid, version=None):
        """
        Get an instance of objType with the supplied guid

        @param objType : type of object to check
        @param guid : unique identifier
        @param version : unique identifier indicating the version of the object. (Optional)
                         If specified, only the mentioned version will be retrieved,
                         If ommited, only the active version is retrieved !
        """
        if not version:
	    sql = "select * from only %s.main where guid='%s'"%(objType,guid)
            errorStr = '%s with guid %s not found.'%(objType, guid)
        else:
	    sql = "select * from %s.main where guid='%s' and version = '%s'"%(objType,guid, version)
            errorStr = '%s with guid %s and version %s not found.'%(objType, guid, version)

	result = self.__executeQuery(sql)
        if not result:
            q.eventhandler.raiseCriticalError(errorStr)
        else:
            result =  result[0]['data'][1:-1]
            return result.decode('hex')


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

    def objectDelete(self, objType, guid, version):
        """
        Delete an instance of objType with the supplied guid

        @param objType : type of object to check
        @param guid : unique identifier
        @param version : unique version for the given guid
        """
        if(self.objectExists(objType, guid, version)):
            if not version:
		sql = "delete from %s.main where guid='%s'"%(objType,guid)
            else:
		sql = "delete from %s.main where guid='%s' and version='%s'"%(objType,guid,version)

	    self.__executeQuery(sql, False)
            return True
        else:
            if not version:
                q.eventhandler.raiseCriticalError('%s with guid %s not found.'%(objType, guid))
            else:
                q.eventhandler.raiseCriticalError('%s with guid %s and version %s not found.'%(objType, guid, version))

    def objectSave(self,data):
        """
        Update or create the supplied object

        @param objType : type of object to check
        @param guid : unique identifier
        """
        if not self.objectExists(data.__class__.__name__, data.guid, None):
            return self._createObject(data)
        else:
            return self._updateObject(data)


    def createObjectType(self, objType):
        """
        Creates the model structure on the database

        @param objType : the object type to create
        """
        objTypeName = objType.__class__.__name__
        self.createObjectTypeByName(objTypeName)

    def createObjectTypeByName(self, objTypeName):
        """
        Creates the model structure on the database

        @param objTypeName : the name of the type to create
        """
        if self.schemeExists(objTypeName):
	    q.logger.log("ObjectType %s already exists"%objTypeName ,3)
	    return

	sqls = ['CREATE SCHEMA %s'%objTypeName, \
		'CREATE TABLE %s.main ( guid uuid NOT NULL, "version" uuid, creationdate timestamp without time zone, data text, CONSTRAINT pk_guid PRIMARY KEY (guid)) WITH (OIDS=FALSE);'%objTypeName, \
#		'CREATE TABLE %(scheme)s.main_archive () INHERITS (%(scheme)s.main) WITH (OIDS=FALSE);'%{'scheme':objTypeName},\
#		'CREATE OR REPLACE RULE %(scheme)s_delete AS ON DELETE TO %(scheme)s.main DO  INSERT INTO %(scheme)s.main_archive (guid, version, creationdate, data) VALUES (old.guid, old.version, old.creationdate, old.data)'%{'scheme':objTypeName},\
#		'CREATE OR REPLACE RULE %(scheme)s_update AS ON UPDATE TO %(scheme)s.main DO  INSERT INTO %(scheme)s.main_archive (guid, version, creationdate, data) VALUES (old.guid, old.version, old.creationdate, old.data)'%{'scheme':objTypeName},
		'CREATE INDEX guid_%(schema)s_main ON %(schema)s.main (guid)'%{'schema':objTypeName}, 'CREATE INDEX version_%(schema)s_main ON %(schema)s.main (version)'%{'schema':objTypeName}]

	for sql in sqls:
	    self.__executeQuery(sql, False)

    def schemeExists(self, name):
        """
        Checks if the schema with the supplied name exists

        @param name : name of the schema to check
        """
        sql =  "select distinct schemaname as name from pg_tables where schemaname = '%s'"%name
        result = self.__executeQuery(sql)
        if result:
            return True
        else:
            return False

    def viewExists(self, objType, viewname):
        """
        Checks if the requested view exists in the supplied schema

        @param objType : the object type to check
        @param viewname : name of the view to check
        """
        sql =  "select distinct schemaname, tablename from pg_tables where schemaname = '%s' and tablename = '%s'"%(objType, viewname)
        result = self.__executeQuery(sql)
        if result:
            return True
        else:
            return False


    def _createObject(self, data):
        """
        Store the supplied data in the database
        @param data : object to store
        """
        data.creationdate = time.strftime('%Y-%m-%d %H:%M', time.localtime())

        obj = data.serialize(ThriftSerializer)
        obj = obj.encode('hex')
        query = "insert into %s.main (guid, version, creationdate, data) VALUES ('%s', '%s', '%s', '{%s}')"%(data.__class__.__name__, data.guid, data.version, data.creationdate, obj)
        try:
	    self.__executeQuery(query, False)
        except ProgrammingError, ex:
            raise OsisException(query, ex)
        return data

    def _updateObject(self, data):
        """
        Update the supplied data in the database

        @param data : object to update
        """
        obj = data.serialize(ThriftSerializer)
        obj = obj.encode('hex')
        query = "update only %s.main set guid = '%s', version = '%s', data = '{%s}' where guid = '%s'"%(data.__class__.__name__, data.guid, data.version, obj, data.guid)
        try:
	    self.__executeQuery(query, False)
        except ProgrammingError, ex:
            raise OsisException(query, ex)
        return data


    def _find_table(self, schema, name):
        try:
	    full_name = '%s.%s' % (schema, name)
            return self._sqlalchemy_metadata.tables[full_name]
        except KeyError:
            pass

        self._sqlalchemy_metadata.reflect(
            bind=self._sqlalchemy_engine, schema=schema, only=(name, ))

        return self._sqlalchemy_metadata.tables[full_name]


    def objectsFind(self, objType, filterobject, viewToReturn=None):
        """
        returns a list of matching guids according to the supplied fitlerobject filters

        @param objType : type of object to search
        @param filterobject : a list of filters indicating the view and field-value to use to filter
        @param viewToReturn : the view to use to return the list of found objects
        """

        # Step 1: turn the filters into a more sane datastructure
        filters = set()
        for filter_ in filterobject.filters:
            view = filter_.keys()[0]
            field = filter_[view].keys()[0]
            value, exact = filter_[view][field]

            filters.add((view, field, value, exact, ))

        filters = tuple(filters)

        # Step 2: Create list of values to retrieve
        if not viewToReturn:
            table_name = 'main'
            table = self._find_table(objType, table_name)
            fields = [table.c.guid]
        else:
            table_name = viewToReturn
            table = self._find_table(objType, table_name)
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
            set(self._find_table(objType, filter_[0]) for filter_ in filters if filter_[0] != table_name),
            table)

        # Step 4: Create 'where' clause
        def create_clause((view, field,value, exact, )):
            table = self._find_table(objType, view)
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


    def objectsFindAsView(self, objType, filterObject, viewName):
        """
        Find
        @param objType : type of object to search
        @param filterobject : a list of filters indicating the view and field-value to use to filter
        @param viewToReturn : the view to use to return the list of found objects
        """
        cols, rows = self.objectsFind(objType, filterObject, viewName)

        return tuple(
            dict((col[0], row[i]) for (i, col) in enumerate(cols)) for row in rows)

    def getFilterObject(self):
        """
        returns an object to hold the filter criteria
        """
        return OsisFilterObject()

    def viewCreate(self, objType, viewName):
        """
        Creates and returns a new view object

        @param objType : the object type on which to add the view
        @param viewName : the name of the view
        """

        if not self.viewExists(objType, viewName):
            return OsisView(objType, viewName)
        else:
            q.eventhandler.raiseCriticalError('[%s] already has a view [%s].'%(objType, viewName))

    def viewAdd(self, view):
        """
        Adds the new view to the database

        @param view : Osisview object to create on the database
        """
	for sql in view.buildSql():
	    self.__executeQuery(sql, False)


    def viewDestroy(self, objType, viewName):
        """
        Removes a view from the database
        @param objType : the type of object to destroy
        @param viewName : Osisview object to destroy
        """
        if not self.viewExists(objType, viewName):
            q.eventhandler.raiseCriticalError('%s.%s not found.'%(objType, viewName))
            return

	sql = 'DROP TABLE %s.%s CASCADE'%(objType, viewName)
	self.__executeQuery(sql, False)
        return True

    def viewDelete(self, objType, viewName, guid, versionguid=None):
        """
        Removes row(s) with the supplied guid from the view

        @param objType : the object Type name
        @param viewName : the view from which to remove a row
        @param viewguid : unique identifier (GUID) for the object
        @param versionguid : unique identifier indicating the version of the object. (Optional)
                             If specified, only the mentioned version will be removed,
                             If ommited, all versions will be removed !
        """

        if not versionguid:
	    sql = "delete from %s.%s where guid='%s'"%(objType, viewName, guid)
        else:
	    sql = "delete from %s.%s where guid='%s' and version = '%s'"%(objType, viewName, guid, versionguid)

	self.__executeQuery(sql, False)
        return True


    def viewSave(self, objType, viewName, guid, version, fields):
        """
        Add a new row to the view

        @param objType : the object Type name
        @param viewName : the view from which to remove a row
        @param guid : unique identifier for the object
        @param versionguid : unique identifier indicating the version of the object
        @param fields : dict containing the field:values or list of dict containing 
                        the field:values if multiple records needs to be updated
        """      
          
        # Remove current entry 
        self.viewDelete(objType, viewName, guid)
        
        # Prepare values        
        newViewGuid = q.base.idgenerator.generateGUID()
        if not isinstance(fields, list):
            fields = [fields,]

        # Add new entry
        table = self._find_table(objType, viewName)
        
        for field in fields:
            # Add missing field data
            field.update({
                'guid': guid,
                'version': version,
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


    def _generateSQLString(self, value):
        if value == None:
            return 'NULL'
        if q.basetype.integer.check(value):
            return value
        if q.basetype.float.check(value):
            return value
        return "'%s'"% value

    def _generateSQLCondition(self, objType, view, field, value, fieldtype, exactMatch=False):
        ret = ""
        if (isinstance(value,dict) and value.has_key('_pm_enumeration_name') and value['_pm_enumeration_name'] == 'None') or (fieldtype in ('uuid') and value in (None, "")):
            ret = "%s.%s.%s is NULL"%(objType,view,field)
        elif fieldtype in  ('uuid', 'bool',):
            ret = "%s.%s.%s = '%s'"%(objType,view,field,value)
        elif fieldtype in ('character varying', 'text', 'datetime'):
	    field = '%s.%s.%s'%(objType,view,field)
	    if fieldtype in ('datetime'):
		field = 'cast(%s as varchar)'%field
	    if exactMatch:
		ret = "%s = '%s'"%(field, self._escape(value))
	    else:
		ret = "%s like '%%%s%%'"%(field, self._escape(value))
        else:
            if q.basetype.integer.check(value) or q.basetype.float.check(value):
                ret = "%s.%s.%s = %s"%(objType,view,field,value)

        return ret

    def _getViewResultAsDict(self, objType, view, results):
        if not results:
            return list()

	columns = self._getColumns(objType, view)
        dataFound = self._getViewData(objType, view, results)

	for data in dataFound:
	    for columnName in [col for col in data if columns[col] in osisPGTypeConverter.requiresConvert]:
		data[columnName] = osisPGTypeConverter.convertValue(columns[columnName], data[columnName])

        return dataFound

    def _getViewResults(self, objType, view, results):
        columns = self._getColumns(objType, view)
        coldef = list()

        for colName, colType in columns.iteritems():
	    coldef.append((colName, osisPGTypeConverter.convertType(colType)))


        #no results to retrieve, just return the view definition
        if not results:
            return tuple(coldef), tuple()

        #retrieve view data

        rawdata = self._getViewData(objType, view, results)

        return tuple(coldef), tuple(rawdata)


    def _getColumns(self, objType, view):
	columns = self._dbConn.listColumns(view, objType)
        return columns

    def _getViewData(self, objType, view, results):
        viewname = "%s.%s"%(objType, view)
        mainname = "%s.main"%objType
        mainguid = "%s.guid"%mainname
        viewguid = "%s.guid"%viewname
        mainversion = "%s.version"%mainname
        viewversion = "%s.version"%viewname

        guids = ','.join("'%s'"%r for r in results)
        sql = """
        select %(viewname)s.* from %(viewname)s
            inner join only %(mainname)s on %(mainguid)s = %(viewguid)s and %(mainversion)s = %(viewversion)s
        where %(viewguid)s in (%(guids)s)"""%{
                'mainname':mainname,
                'mainguid':mainguid,
                'viewname':viewname,
                'viewguid':viewguid,
                'mainversion':mainversion,
                'viewversion':viewversion,
                'guids':guids}

	rawdata = self.__executeQuery(sql)
        return rawdata

    def _getFiltersResults(self, objType, filterQueries):
	conditions = list()
	sql = ""
	for index, view in enumerate(filterQueries):
	    conditions.extend(filterQueries[view])
	    if index == 0:
		firstview = view
		sql = "select %(obj)s.%(firstview)s.guid from %(obj)s.%(firstview)s"%{'obj':objType, 'firstview':firstview}
		continue
	    sql += " inner join %(obj)s.%(view)s on %(obj)s.%(view)s.guid = %(obj)s.%(firstview)s.guid"%{'obj':objType, 'view':view, 'firstview': firstview}

	if not sql: return list()
	sql += " inner join only %(obj)s.main on %(obj)s.main.guid = %(obj)s.%(firstview)s.guid and %(obj)s.main.version = %(obj)s.%(firstview)s.version"%{'obj':objType, \
																			   'firstview':firstview}
	sql += " where %s"%(" and ".join(conditions))
	result = self.__executeQuery(sql)
	return [row['guid'] for row in result]

    def _escape(self, pgstr):
        pgstr = pgstr.replace("'", "\\'")
        return pgstr


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
        raise NotImplementedError
        return OsisConnectionPG8000()
    else:
        return OsisConnectionPYmonkeyDBConnection()
    # else uses PYmonkeyDBConnection one
    #return OsisConnectionPYmonkeyDBConnection()
