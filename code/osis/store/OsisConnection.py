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

from osis.model.serializers import ThriftSerializer
from pg import ProgrammingError
import exceptions
import traceback
import uuid

from pymonkey.decorators import deprecated

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

    def connect(self, ip, db, login, passwd):
        """
        Connect to the postgresql server

        @param ip : ip of the db server
        @param db : database to connect to
        @param login : login to connect
        @param passwd : password to connect
        """
        raise Exception("unimplemented generic connect")


    @deprecated
    def objectExists(self, objType, guid, version):
        """
        Checks if an instance of objType with the supplied guid exists

        @param objType : type of object to check
        @param guid : unique identifier
        @param version : unique version for the given guid
        """
        pass

    @deprecated
    def viewObjectExists(self, objType, viewName, guid, version):
        """
        Checks if an instance of objType with the supplied guid exists

        @param objType : type of object to check
        @param viewName : view whixh contains the object
        @param guid : unique identifier
        @param version : unique version for the given guid
        """
        pass

    @deprecated
    def objectGet(self, objType,guid, version=None):
        """
        Get an instance of objType with the supplied guid

        @param objType : type of object to check
        @param guid : unique identifier
        @param version : unique identifier indicating the version of the object. (Optional)
                         If specified, only the mentioned version will be retrieved,
                         If ommited, only the active version is retrieved !
        """
        pass


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

    @deprecated
    def objectDelete(self, objType, guid, version):
        """
        Delete an instance of objType with the supplied guid

        @param objType : type of object to check
        @param guid : unique identifier
        @param version : unique version for the given guid
        """
        pass

    @deprecated
    def objectSave(self,data):
        """
        Update or create the supplied object

        @param objType : type of object to check
        @param guid : unique identifier
        """
        pass


    def createObjectType(self, objType):
        """
        Creates the model structure on the database

        @param objType : the object type to create
        """
        objTypeName = objType.__class__.__name__
        self.createObjectTypeByName(objTypeName)

    def schemeCreate(self, name):
        """
        Creates the model structure on the database

        @param objTypeName : the name of the type to create
        """
        if self.schemeExists(name):
            q.logger.log("Schema %s already exists"%name ,3)
            return

        sqls = ['CREATE SCHEMA %s'%name]
        
        #, \
        #'CREATE TABLE %s.main ( guid uuid NOT NULL, "version" uuid, creationdate timestamp without time zone, data text, CONSTRAINT pk_guid PRIMARY KEY (guid)) WITH (OIDS=FALSE);'%objTypeName, \
        #'CREATE TABLE %(scheme)s.main_archive () INHERITS (%(scheme)s.main) WITH (OIDS=FALSE);'%{'scheme':objTypeName},\
        #'CREATE OR REPLACE RULE %(scheme)s_delete AS ON DELETE TO %(scheme)s.main DO  INSERT INTO %(scheme)s.main_archive (guid, version, creationdate, data) VALUES (old.guid, old.version, old.creationdate, old.data)'%{'scheme':objTypeName},\
        #'CREATE OR REPLACE RULE %(scheme)s_update AS ON UPDATE TO %(scheme)s.main DO  INSERT INTO %(scheme)s.main_archive (guid, version, creationdate, data) VALUES (old.guid, old.version, old.creationdate, old.data)'%{'scheme':objTypeName},
        #'CREATE INDEX guid_%(schema)s_main ON %(schema)s.main (guid)'%{'schema':objTypeName}, 'CREATE INDEX version_%(schema)s_main ON %(schema)s.main (version)'%{'schema':objTypeName}]

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
        
        if not self.schemeExists(objType):
            return False
        
        sql =  "select distinct schemaname, tablename from pg_tables where schemaname = '%s' and tablename = '%s'"%(objType, viewname)
        result = self.__executeQuery(sql)
        if result:
            return True
        else:
            return False

    def objectsFind(self, objType, filterobject, viewToReturn):
        """
        returns a list of matching guids according to the supplied fitlerobject filters

        @param objType : type of object to search
        @param filterobject : a list of filters indicating the view and field-value to use to filter
        @param viewToReturn : the view to use to return the list of found objects
        """
        results =self._find(objType, filterobject, viewToReturn)

        if viewToReturn:
            q.logger.log("Building view %s"%viewToReturn ,3)
            results = self._getViewResults(objType, viewToReturn, results)

        return results

    def _find(self, objType, filterobject, viewToReturn):
        '''
        @todo: remove ugly hack for find without view!
        
        '''
        results = []

        if viewToReturn:
            sql = "select guid from %s.%s"%(objType, viewToReturn)
        else:
            sql = "select guid from %s.view_%s_list" % (objType, objType)


        
        rawdata = self.__executeQuery(sql)

        for row in rawdata:
            results.append(row['guid'])

        filterQueries = dict()

        for item in filterobject.filters:
            view = item.keys()[0]
            columns = self._getColumns(objType, view)
            value = item.get(view)
            field = value.keys()[0]
            fieldtype = columns.get(field, None)
            
            if not fieldtype:raise OsisException('columns.get(%s) from view %s.%s'%(fieldtype, objType, view), 'Column %s does not exist in view %s.%s'%(field, objType, view))
            fieldvalue, exactMatch = value.get(field)
            
            query = filterQueries.get(view, list())
            query.append(self._generateSQLCondition(objType, view, field , fieldvalue, fieldtype, exactMatch))
            filterQueries[view] = query

        if filterQueries:results = self._getFiltersResults(objType, filterQueries)
        
        return list(set(results))

    def objectsFindAsView(self, objType, filterObject, viewName):
        """
        Find
        @param objType : type of object to search
        @param filterobject : a list of filters indicating the view and field-value to use to filter
        @param viewToReturn : the view to use to return the list of found objects
        """
        results = self._find(objType, filterObject, viewName)
        return self._getViewResultAsDict(objType, viewName, results)

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

        if not self.schemeExists(objType):
            self.schemeCreate(objType)

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
        @param versionguid : unique identifier indicating the version of the object. (OBSOLETED)
                             If specified, only the mentioned version will be removed,
                             If ommited, all versions will be removed !
        """

        sql = "delete from %s.%s where guid='%s'" % (objType, viewName, guid)
        
        self.__executeQuery(sql, False)
        return True


    def viewSave(self, objType, viewName, guid, version, fields):
        """
        Add a new row to the view

        @param objType : the object Type name
        @param viewName : the view from which to remove a row
        @param guid : unique identifier for the object
        @param versionguid : unique identifier indicating the version of the object (OBSOLETED)
        @param fields : dict containing the field:values
        """
        
        
        # @todo: do this transactional!
        # update == delete + insert
        self.viewDelete(objType, viewName, guid)
        
        
        fieldnames = "guid, viewguid"
        values = "'%s', '%s'"%(guid, q.base.idgenerator.generateGUID())

        for itemKey in fields.iterkeys():
            fieldnames = "%s, %s"%(fieldnames, itemKey)
            if fields[itemKey]:
                if type(fields[itemKey]) is str:
                    values = "%s, '%s'"%(values,  self._escape(fields[itemKey]))
                else:
                    values = "%s, '%s'"%(values,  fields[itemKey])
            else:
                values = "%s, %s"%(values, self._generateSQLString(fields[itemKey]))

        sql = "insert into %s.%s (%s) VALUES (%s)"%(objType, viewName, fieldnames, values)
        try:
            self.__executeQuery(sql, False)
        except ProgrammingError, ex:
            raise OsisException(sql, ex)

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
                field = 'cast(%s as varchar)' % field
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


    # @todo: remove reference to viewguid!
    def _getViewData(self, objType, view, results):
        viewname = "%s.%s"%(objType, view)
        viewguid = "%s.guid"%viewname

        guids = ','.join("'%s'"%r for r in results)
        sql = """
        select %(viewname)s.* from %(viewname)s
        where %(viewguid)s in (%(guids)s)"""%{
                'viewname':viewname,
                'viewguid':viewguid,
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
        #sql += " inner join only %(obj)s.main on %(obj)s.main.guid = %(obj)s.%(firstview)s.guid and %(obj)s.main.version = %(obj)s.%(firstview)s.version"%{'obj':objType, \
        #                                                                           'firstview':firstview}
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

class OsisConnectionPYmonkeyDBConnection(OsisConnectionGeneric):
    def connect(self, ip, db, login, passwd):
        self._dbConn = DBConnection(ip, db, login, passwd)
        self._login = login
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