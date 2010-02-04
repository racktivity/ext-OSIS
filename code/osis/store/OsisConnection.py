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
from database.jdbthrift.ttypes import KeyValueException
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
        self._jugConn = None
        self._login = None
        self._versionListKey = "VERSION_LIST"

    def _createJuggernautDbConnection(self, ip, port, namespace, passwd, masterkey=""):
        """
        create a JuggernautDb namespace connection

        @param ip : ip of the db server
        @port : port to be connected with JuggernautDb
        @param namespace : namespace to be connected
        @param login : login to connect
        @param passwd : password to connect
        """
        # TODO --> Remove the login which is not required.

    	q.logger.log("in createJuggernautDbConnection() function", 5)
        connection = q.jdb.client.getJDBClusterConnection(ip, int(port))
        if namespace not in connection.listSpaces():
            connection.createNamespace(namespace, passwd, masterkey)
        namespaceConnection=connection.getNamespaceConnection(namespace, passwd)

        return namespaceConnection

    def connect(self, ip, namespace, login, passwd, master, port,
                        pgsip, pgsdb, pgslogin, pgspasswd):
        """
        Connect to the postgresql server

        @param ip : ip of the db server
        @param namespace : database to connect to
        @param login : login to connect
        @param passwd : password to connect
        """
        self._jugConn = self._createJuggernautDbConnection(ip, port, namespace, passwd, master)
        self._dbConn = DBConnection(pgsip, pgsdb, pgslogin, pgspasswd)
        self._login = login


    def objectExists(self, objType, guid, version, blnQuick = False):
        """
        Checks if an instance of objType with the supplied guid exists

        @param objType : type of object to check
        @param guid : unique identifier
        @param version : unique version for the given guid
        """
        q.logger.log("in objectExists() function ", 5)

        dctObj = None
        try:
            dctObj = self._jugConn.get(guid)
            if blnQuick: return dctObj # This is just to verify does the id exists or not

            if version:
                return dctObj[version]
            else:
                version = dctObj[self._versionListKey][-1]
                if version:
                    return dctObj[version]
                else:
                    return None
        except KeyValueException:
            q.logger.log("Object does not exist with the id", 5)
            return None
        except KeyError:
            q.logger.log("Object does not exist with the given version", 5)
            return None
    

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


    def objectGet(self, objType, guid, version=None):
        """
        Get an instance of objType with the supplied guid

        @param objType : type of object to check
        @param guid : unique identifier
        @param version : unique identifier indicating the version of the object. (Optional)
                         If specified, only the mentioned version will be retrieved,
                         If ommited, only the active version is retrieved !
        """
        q.logger.log("objectGet() function call invoked", 5)

        result = self.objectExists(objType, guid, version)
        if not result:
            q.eventhandler.raiseCriticalError(errorStr)
        else:
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


    def _jugobjectDelete(self, objType, guid, version):
        """
            Delete an instance of objType with the supplied guid

            @param objType : type of object to check
            @param guid : unique identifier
            @param version : unique version for the given guid
        """
        q.logger.log("objectDelete() function call invoked", 5)
        
        dctObject = self.objectExists(objType, guid, None, blnQuick=True)
        if dctObject:
            if not version:
                self._jugConn.remove(guid)
                self._jugConn.put("deleted__%s" % guid, dctObject)
                q.logger.log("deletion completed succesfully", 5)
                return True
            try:
                dctObject[self._versionListKey].remove(version)
                if not dctObject[self._versionListKey]:
                    self._jugConn.remove(guid)
                    dctObject[self._versionListKey].append(version)
                    self._jugConn.put("deleted__%s" % guid, dctObject)
                    return True
                dctObject["deleted__%s" % version] = dctObject[version]
                del dctObject[version]
            except:
                q.eventhandler.raiseCriticalError('%s with guid %s and version %s not found.'%(objType, guid, version))
                return False
            self._jugConn.modify(guid, dctObject)
            q.logger.log("deletion completed succesfully is completed", 5)
            return True
        else:
            q.eventhandler.raiseCriticalError('%s with guid %s not found.'%(objType, guid))


    def objectDelete(self, objType, guid, version):
        """
        Delete an instance of objType with the supplied guid

        @param objType : type of object to check
        @param guid : unique identifier
        @param version : unique version for the given guid
        """
        self._jugobjectDelete(objType, guid, version)
        

    def _jugobjectSave(self,data):
        """
        Update or create the supplied object

        @param objType : type of object to check
        @param guid : unique identifier
        """
        q.logger.log("objectSave() function invoked", 5)

        dctObjectToSave = self.objectExists(data.__class__.__name__, data.guid, None, blnQuick=True)
        if not dctObjectToSave:
            return self._jugcreateObject(data)
        else:
            return self._jugupdateObject(data, dctObjectToSave)
    

    def objectSave(self,data):
        """
        Update or create the supplied object

        @param objType : type of object to check
        @param guid : unique identifier
        """
        self._jugobjectSave(data)


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
        sql =  "select distinct schemaname, tablename from pg_tables where schemaname = '%s' and tablename = '%s'"%(str(objType).lower(), viewname)

        q.logger.log("Going to check wheather the view exists or not", 5)
        q.logger.log(sql, 5)

        result = self._dbConn.sqlexecute(sql).dictresult()
        if result:
            return True
        else:
            return False


    def _jugcreateObject(self, data):
        """
        Store the supplied data in the database
        @param data : object to store
        """
        q.logger.log("_CreateObject() function call invoked", 5)

        data.creationdate = time.strftime('%Y-%m-%d %H:%M', time.localtime())

        obj = data.serialize(ThriftSerializer)
        obj = obj.encode('hex')

        dctToWrite = {  data.version: obj,
                        self._versionListKey: [data.version]
                        }

        try:
            self._jugConn.put(data.guid, dctToWrite)
            q.logger.log("self._jugConn.put(key, dctToWrite) is completed", 5)
        except ProgrammingError, ex:
            raise OsisException(key, ex)
        return data


    def _jugupdateObject(self, data, dctObjectToSave):
        """
        Update the supplied data in the database

        @param data : object to update
        """
        q.logger.log("updateObject() function call invoked", 5)
        data.creationdate = time.strftime('%Y-%m-%d %H:%M', time.localtime())

        obj = data.serialize(ThriftSerializer)
        obj = obj.encode('hex')

        try:
            dctObjectToSave[self._versionListKey].remove(data.version)
        except:
            pass
        dctObjectToSave[self._versionListKey].append(data.version)
        dctObjectToSave[data.version] = obj

        try:
            self._jugConn.modify(data.guid, dctObjectToSave)
            q.logger.log("self._jugConn.modify(key, obj) is completed", 5)
        except ProgrammingError, ex:
            raise OsisException(key, ex)
        

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

        actualResults = []
        for guid in results:
            if self.objectExists(objType, guid, None):
                actualResults.append(guid)

        if viewToReturn:
            q.logger.log("Building view %s"%viewToReturn ,3)
            results = self._getViewResults(objType, filterobject, actualResults)

        return actualResults

    def _find(self, objType, filterobject, viewToReturn):
	results = []
        for eachDict in filterobject.filters:
            tableName = eachDict.keys()[0]
            columnName = eachDict[tableName].keys()[0]
            value = eachDict[tableName][columnName]
            if type(value) == type(''):
                value = "'%s'" % value
            sql = """select guid from %s.%s where %s = %s""" % (objType, tableName, columnName, value)
            q.logger.log("Going to execute the following sql query..", 5)
            q.logger.log(sql, 5)
            q.logger.log("Query executed successfully..", 5)

            rawdata = self._dbConn.sqlexecute(sql).dictresult()
            for row in rawdata:
                results.append(row['guid'])
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
            q.logger.log(sql, 5)
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

    def _getViewResults(self, objType, filterobject, results):
        columns = []
        for eachDict in filterobject.filters:
            tableName = eachDict.keys()[0]
            columns += self._getColumns(objType, tableName)
        coldef = list()

        for col in columns:
	    coldef.append((col[0], osisPGTypeConverter.convertType(col[1])))

        q.logger.log("in _getViewResults() function.... ")
        q.logger.log("The columns are:  %s"% str(coldef), 5)

        #no results to retrieve, just return the view definition
        if not results:
            return tuple(coldef), tuple()

        #retrieve view data

        rawdata = []
        for eachDict in filterobject.filters:
            view = eachDict.keys()[0]
            rawdata += self._getViewData(objType, view, results)

        return tuple(coldef), tuple(rawdata)


    def _getColumns(self, objType, view):
        colList= """
        select column_name, data_type
           from information_schema.columns
           where table_name = '%s' and table_schema = '%s'
        """%(view, objType)

        q.logger.log("In _getColumns() function...")
        q.logger.log("The query to execute is:  %s"% str(colList), 5)
        columns = self._dbConn.sqlexecute(colList).getresult()
        q.logger.log("Resultant columns:  %s"% str(columns), 5)
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
            where %(viewguid)s in (%(guids)s)"""%{
                'viewname':viewname,
                'viewguid':viewguid,
                'guids':guids}

        q.logger.log("Going to execute _getViewData() function with following query..")
        q.logger.log("%s"% str(sql), 5)
        
        rawdata = self._dbConn.sqlexecute(sql).getresult()
        q.logger.log("%s is the result set of the following operation..."% str(rawdata), 5)

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





