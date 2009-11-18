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
from pymonkey.db.DBConnection import DBConnection
from OsisView import OsisView, OsisColumn, OsisType
from OsisFilterObject import OsisFilterObject

from osis.model.serializers import ThriftSerializer
from pg import ProgrammingError
import exceptions
import traceback

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
        self._pgType2pyType["uuid"] = "uuid"
        self._pgType2pyType["timestamp without time zone"] = "datetime"
        self._pgType2pyType["boolean"] = "bool"
        self._pgType2pyType["ARRAY"] = "hex"

    def convertType(self, pgType):
        return self._pgType2pyType[pgType]

    def convertValue(self, pgType, pgValue):
	pyType = self.convertType(pgType)
	if pgType == 'boolean':
	    if 'f' in pgValue:
		return False
	    elif 't' in pgValue:
		return True
	return pgValue

    def convertToPg(self, pyType, value):
	if not value:
	    if pyType == 'integer':
		value =  0
	    elif pyType == 'bool':
		value =False
	#else:
	    #return eval("%s(%s)"%(pyType, pgValue))


osisPGTypeConverter = _OsisPGTypeConverter()

class OsisConnection(object):
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
        self._dbConn = DBConnection(ip, db, login, passwd)
        self._login = login


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
            q.logger.log("select * from only %s.%s where guid='%s'"%(objType, viewName, guid) ,5)
            result = self._dbConn.sqlexecute("select * from only %s.%s where guid='%s'"%(objType, viewName, guid)).dictresult()
        else:
            q.logger.log("select * from %s.%s where guid='%s' and version='%s'"%(objType, viewName, guid, version) ,5)
            result = self._dbConn.sqlexecute("select * from %s.%s where guid='%s' and version='%s'"%(objType, viewName, guid, version)).dictresult()

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
            result = self._dbConn.sqlexecute("select * from only %s.main where guid='%s'"%(objType,guid)).dictresult()
            errorStr = '%s with guid %s not found.'%(objType, guid)
        else:
            result = self._dbConn.sqlexecute("select * from %s.main where guid='%s' and version = '%s'"%(objType,guid, version)).dictresult()
            errorStr = '%s with guid %s and version %s not found.'%(objType, guid, version)
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
	    result= self._dbConn.sqlexecute(query)
	    if result:
		return result.dictresult()
	    return dict()
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
                self._dbConn.sqlexecute("delete from %s.main where guid='%s'"%(objType,guid))
            else:
                self._dbConn.sqlexecute("delete from %s.main where guid='%s' and version='%s'"%(objType,guid,version))
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
        if not self.schemeExists(objTypeName):
            q.logger.log("Creating object schema in database" ,3)
            self._dbConn.sqlexecute('CREATE SCHEMA %s'%objTypeName)
            q.logger.log("Creating object main table in database" ,3)
            self._dbConn.sqlexecute('CREATE TABLE %s.main ( guid uuid NOT NULL, "version" uuid, creationdate timestamp without time zone, data text, CONSTRAINT pk_guid PRIMARY KEY (guid)) WITH (OIDS=FALSE);'%objTypeName)
            q.logger.log("Creating object main archive table in database" ,3)
            self._dbConn.sqlexecute('CREATE TABLE %(scheme)s.main_archive () INHERITS (%(scheme)s.main) WITH (OIDS=FALSE);'%{'scheme':objTypeName})
            q.logger.log("Creating delete rule in database" ,3)
            self._dbConn.sqlexecute('CREATE OR REPLACE RULE %(scheme)s_delete AS ON DELETE TO %(scheme)s.main DO  INSERT INTO %(scheme)s.main_archive (guid, version, creationdate, data) VALUES (old.guid, old.version, old.creationdate, old.data)'%{'scheme':objTypeName})
            q.logger.log("Creating update rule in database" ,3)
            self._dbConn.sqlexecute('CREATE OR REPLACE RULE %(scheme)s_update AS ON UPDATE TO %(scheme)s.main DO  INSERT INTO %(scheme)s.main_archive (guid, version, creationdate, data) VALUES (old.guid, old.version, old.creationdate, old.data)'%{'scheme':objTypeName})
        else:
            q.logger.log("ObjectType %s already exists"%objTypeName ,3)
    def schemeExists(self, name):
        """
        Checks if the schema with the supplied name exists

        @param name : name of the schema to check
        """
        sql =  "select distinct schemaname as name from pg_tables where schemaname = '%s'"%name
        result = self._dbConn.sqlexecute(sql).dictresult()
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
        result = self._dbConn.sqlexecute(sql).dictresult()
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
	    self._dbConn.sqlexecute(query)
	except ProgrammingError, ex:
	    raise OsisException(query, ex)
        return data

    def _updateObject(self, data):
        """
        Update the supplied data in the database

        @param data : object to update
        """
        data.creationdate = time.strftime('%Y-%m-%d %H:%M', time.localtime())
        obj = data.serialize(ThriftSerializer)
        obj = obj.encode('hex')
	query = "update only %s.main set guid = '%s', version = '%s', creationdate = '%s', data = '{%s}' where guid = '%s'"%(data.__class__.__name__, data.guid, data.version, data.creationdate, obj, data.guid)
	try:
	    self._dbConn.sqlexecute(query)
	except ProgrammingError, ex:
	    raise OsisException(query, ex)
        return data

    def objectsFind(self, objType, filterobject, viewToReturn=None):
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
	results = []

        if viewToReturn:
            sql = "select guid from %s.%s"%(objType, viewToReturn)
        else:
            sql = "select guid from only %s.%s"%(objType, 'main')

        rawdata = self._dbConn.sqlexecute(sql).dictresult()
        for row in rawdata:
            results.append(row['guid'])

        for item in filterobject.filters:
            view = item.keys()[0]
	    columns = self._getColumns(objType, view)
            field = item.values()[0].keys()[0]
	    fieldtype = [column[1] for column in columns if column[0] == field][0]
            fieldvalue = item.values()[0].values()[0]
            q.logger.log("Process Filter : (%s.%s = %s)"%(view, field, fieldvalue) ,3)
            results = self._getFilterResults(objType, view, field , fieldvalue, fieldtype, results)
	return results

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

        if not self.viewExists(objType, viewName):
            return OsisView(objType, viewName)
        else:
            q.eventhandler.raiseCriticalError('[%s] already has a view [%s].'%(objType, viewName))

    def viewAdd(self, view):
        """
        Adds the new view to the database

        @param view : Osisview object to create on the database
        """
        self._dbConn.sqlexecute(view.buildSql())


    def viewDestroy(self, objType, viewName):
        """
        Removes a view from the database
        @param objType : the type of object to destroy
        @param viewName : Osisview object to destroy
        """
        if not self.viewExists(objType, viewName):
            q.eventhandler.raiseCriticalError('%s.%s not found.'%(objType, viewName))
            return

        self._dbConn.sqlexecute('DROP TABLE %s.%s CASCADE'%(objType, viewName))
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
            self._dbConn.sqlexecute("delete from %s.%s where guid='%s'"%(objType, viewName, guid))
        else:
            self._dbConn.sqlexecute("delete from %s.%s where guid='%s' and version = '%s'"%(objType, viewName, guid, versionguid))

        return True


    def viewSave(self, objType, viewName, guid, version, fields):
        """
        Add a new row to the view

        @param objType : the object Type name
        @param viewName : the view from which to remove a row
        @param guid : unique identifier for the object
        @param versionguid : unique identifier indicating the version of the object
        @param fields : dict containing the field:values
        """

	columns = self._getColumns(objType, viewName)
        fieldnames = "guid, version, viewguid"
        values = "'%s', '%s', '%s'"%(guid, version, q.base.idgenerator.generateGUID())

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
	    self._dbConn.sqlexecute(sql)
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

    def _checkValues(self, pyValue):
	if pyValue == None:
	    return 'NULL'
	return pyValue
	#return _OsisPGTypeConverter().convertToPg(pyType, pyValue)

    def _generateSQLCondition(self, objType, view, field, value, fieldtype):
        ret = ""
	if fieldtype in  ('uuid', 'boolean'):
	    ret = "%s.%s.%s = '%s'"%(objType,view,field,value)
	elif fieldtype == 'character varying':
	    ret = "%s.%s.%s like '%%%s%%'"%(objType,view,field, self._escape(value))
	else:
	    if q.basetype.integer.check(value) or q.basetype.float.check(value):
		ret = "%s.%s.%s = %s"%(objType,view,field,value)
        return ret

    def _getViewResultAsDict(self, objType, view, results):
	columnNames = self._getColumns(objType, view)
	if not results:
	    return list()

	dataFound = self._getViewData(objType, view, results)

	result = list()
	for data in dataFound:
	    resultDict = dict()
	    #resultDict = resultDict.fromkeys(columnNames)
	    for index in xrange(len(columnNames)):
		columnName = columnNames[index][0]
		columnType = columnNames[index][1]
		if not data[index] == None:
		    resultDict[columnName] = _OsisPGTypeConverter().convertValue(columnType, data[index])
		else:
		    resultDict[columnName] = ''

	    result.append(resultDict)

	return result

    def _getViewResults(self, objType, view, results):
	columns = self._getColumns(objType, view)
	coldef = list()

        for col in columns:
	    coldef.append((col[0], osisPGTypeConverter.convertType(col[1])))


        #no results to retrieve, just return the view definition
        if not results:
            return tuple(coldef), tuple()

        #retrieve view data

        rawdata = self._getViewData(objType, view, results)

        return tuple(coldef), tuple(rawdata)


    def _getColumns(self, objType, view):
        colList= """
        select column_name, data_type
           from information_schema.columns
           where table_name = '%s' and table_schema = '%s'
        """%(view, objType.lower())

        columns = self._dbConn.sqlexecute(colList).getresult()
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

        rawdata = self._dbConn.sqlexecute(sql).getresult()
	return rawdata

    def _getFilterResults(self, objType, view, filterField, filterValue, fieldType, results):
        #no results left to filter on
        if not results:
            return []

        #no view specified to filter on, so just return the results
        if not view:
            return results

        guidList = []

        guids = ','.join("'%s'"%r for r in results)
        viewname = "%s.%s"%(objType, view)
        mainname = "%s.main"%objType
        mainguid = "%s.guid"%mainname
        viewguid = "%s.guid"%viewname
        mainversion = "%s.version"%mainname
        viewversion = "%s.version"%viewname

        sql = """
        select %(viewguid)s from %(viewname)s
            inner join only %(mainname)s on %(mainguid)s = %(viewguid)s and %(mainversion)s = %(viewversion)s
        where %(filterCondition)s and
              %(viewguid)s in (%(guids)s)"""%{
                'mainname':mainname,
                'viewname':viewname,
                'mainguid':mainguid,
                'viewguid':viewguid,
                'mainversion':mainversion,
                'viewversion':viewversion,
                'filterCondition':self._generateSQLCondition(objType,view,filterField, filterValue, fieldType),
                'guids':guids}

        rawdata = self._dbConn.sqlexecute(sql).dictresult()
        for row in rawdata:
            guidList.append(row['guid'])

        return guidList

    def _escape(self, pgstr):
        pgstr = pgstr.replace("'", "\\'")
        return pgstr





