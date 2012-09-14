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
from OsisView import OsisView
from OsisFilterObject import OsisFilterObject

from pymodel.serializers import ThriftSerializer
from pg import ProgrammingError
import exceptions
import traceback
import threading
import itertools
import datetime
import sqlalchemy

#pylint: disable=E1103

class OsisException(exceptions.Exception):
    def __init__(self, command, msg):
        super(OsisException, self).__init__()

        msg = self.handleException(command, msg)
        self.errmsg = msg
        self.args = (msg,)

    def handleException(self, command, msg): #pylint: disable=W0613
        errorMsg = 'Exception occurred while executing \"%s\".\n' % command
        errorMsg += traceback.format_exc()
        return errorMsg

_SA_CACHE = dict()

class OsisConnection(object):
    def __init__(self, dbtype):
        self._dbConn = None
        self._login = None
        self._lock = threading.Lock()
        self._lock_metadata = threading.Lock()
        self._dbtype = dbtype
        self._sqlalchemy_engine = None
        self._sqlalchemy_metadata = None
        self._sequences = {} #this will be set after the connection is made, in OsisDB module

    def processSequences(self, sequences):
        """
        returns a mapping between table names and sequences, as for oracle we always have to put sequences to tables on reflection
        """
        info = {}
        for domain, table in sequences.iteritems():
            for tblName in table:
                tableName = self._getTableName(domain, tblName)
                schemaName = self._getSchemeName(domain, tblName)
                fullTblName = '%s.%s' % (schemaName, tableName)
                info[fullTblName] = table[tblName]
        self._sequences = info
        
    def getEngine(self):
        return self._sqlalchemy_engine

    def connect(self, ip, port, db, login, passwd, poolsize=10):
        """
        Connect to the sql server

        @param ip : ip of the db server
        @param db : database to connect to
        @param login : login to connect
        @param passwd : password to connect
        @param poolsize : the size of the internal connection pool
        """
        self._login = login
        dsn = '%(dbtype)s://%(user)s:%(password)s@%(host)s:%(port)s/%(db)s' % {
            'host'     : ip,
            'port'     : port,
            'user'     : login,
            'password' : passwd,
            'db'       : db,
            'dbtype'   : self._dbtype
        }

        if dsn not in _SA_CACHE:
            _SA_CACHE[dsn] = {
                "engine": sqlalchemy.create_engine(dsn, pool_size=poolsize),
                "metadata": sqlalchemy.MetaData()
            }

        alchemyInfo = _SA_CACHE[dsn]
        self._sqlalchemy_engine = alchemyInfo["engine"]
        self._sqlalchemy_metadata = alchemyInfo["metadata"]

        return dict()

    def runQuery(self, query, *args, **kwargs):
        '''Run query from OSIS server

        @param query: Query to execute on OSIS server
        @type query: string

        @return: result of the query else raise error
        @type: List of rows. Each row shall be represented as a dictionary.
        '''
        try:
            if args or kwargs:
                return self._executeQuery(query, True, *args, **kwargs)
            else:
                return self._executeQuery(query.replace('%', '%%'))
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
        if not self.schemeExists(domain, objTypeName):
            self.schemeCreate(domain, objTypeName)

        #create rootobject table to store our binary blob
        tableName = objTypeName + "_obj"

        if self.findTable(domain, tableName) is None:
            table = sqlalchemy.Table(self._getTableName(domain, tableName), self._sqlalchemy_metadata,
                sqlalchemy.Column("guid", sqlalchemy.String(46), primary_key=True, nullable=False),
                sqlalchemy.Column("creationdate", sqlalchemy.DateTime()),
                sqlalchemy.Column("data", sqlalchemy.LargeBinary),
                schema=self._getSchemeName(domain, objTypeName)
            )

            if not table.exists(self._sqlalchemy_engine):
                table.create(self._sqlalchemy_engine)

    def _getTableName(self, domain, objType): #pylint: disable=W0613
        """
        Get the table name

        @param domain : name of the domain
        @param objType : name of the object type
        """
        raise NotImplementedError("unimplemented generic connect")

    def _getSchemeName(self, domain, objType): #pylint: disable=W0613
        """
        Get the scheme name

        @param domain : name of the domain
        @param objType : name of the object type
        """
        raise NotImplementedError("unimplemented generic connect")

    def getTableName(self, domain, objType): #pylint: disable=W0613)
        """
        just for exposing getTableName
        """
        return self._getTableName(domain, objType)

    def getSchemeName(self, domain, objType): #pylint: disable=W0613
        return self._getSchemeName(domain, objType)

    def schemeCreate(self, domain, name): #pylint: disable=W0613
        """
        Creates the model structure on the database

        @param domain : domain to create the scheme in
        @param objTypeName : the name of the type to create
        """
        raise NotImplementedError("unimplemented generic connect")

    def schemeExists(self, domain, name): #pylint: disable=W0613
        """
        Checks if the schema with the supplied name exists

        @param domain : domain to check for the schema
        @param name : name of the schema to check
        """
        raise NotImplementedError("unimplemented generic connect")

    def viewExists(self, domain, objType, viewname):
        """
        Checks if the requested view exists in the supplied schema

        @param domain : domain where the view lives
        @param objType : the object type to check
        @param viewname : name of the view to check
        """

        if not self.schemeExists(domain, objType):
            return False

        if self.findTable(domain, viewname) is not None:
            return True
        else:
            return False
        
    def findTable(self, domain, name = None):
        """
        @param name: if None, all tables in the domain will be reflected and return a list with them
                    if string, a table object will be returned
                    if list, a list of table objects will be returned
        """
        schema = self._getSchemeName(domain, name)
        tableList = [] #what we search for
        notFound = False #indicates if at least one table from the requested tables is not yet in metadata
        foundTables = [] #what table objects we already found in db
        #we build the table name list
        if isinstance(name, basestring):
            tableList.append(name)
        else:
            tableList = name
        
        #we ask if the tables already exist
        self._lock_metadata.acquire(True) #I don't know if this is necessary, maybe it is legacy code from pylabs
        if isinstance(tableList, list): #it will be a list unless name is None
            for idx, tableName in enumerate(tableList):
                tableList[idx]  = self._getTableName(domain, tableName)
                fullName = "%s.%s" % (schema, tableName)
                tblObj = self._sqlalchemy_metadata.tables.get(fullName, None)
                if tblObj is not None:
                    foundTables.append(tblObj)
                else:
                    notFound = True
                    
        #we already return, if everything was found
        if not notFound and tableList:
            self._lock_metadata.release()
            if isinstance(name, basestring):
                return foundTables[0]
            return foundTables
        
        #we reflect         
        if notFound or not tableList:
            try:
                self._sqlalchemy_metadata.reflect(bind=self._sqlalchemy_engine, schema=schema, only=tableList)
            except sqlalchemy.exc.DBAPIError, e:
                if not e.connection_invalidated:
                    raise
                self._sqlalchemy_engine.dispose()
                self._sqlalchemy_metadata.reflect(bind=self._sqlalchemy_engine, schema=schema, only=tableList)
            except sqlalchemy.exc.InvalidRequestError: #if the requested table doesn't exist we will return None, is this ok???
                return None
            finally:
                self._lock_metadata.release()
        else:
            self._lock_metadata.release()
        
        #we calculate what to return
        if tableList is None: #this means we reflected everything inside the domain
            tableList = self._sqlalchemy_metadata.tables.keys()
        else:
            tableList = ["%s.%s" % (schema, tableName) for tableName in tableList]
            
        info = []
        for tableName in tableList:
            tblObj = self._sqlalchemy_metadata.tables[tableName]
            info.append(tblObj)
            if self._dbtype == 'oracle': #for oracle we also have to add sequences
                sequence = self._sequences.get(tableName, {})
                for colName, seqName in sequence.iteritems():
                    colObj = getattr(tblObj.c, colName)
                    if not colObj.default:
                        colObj.default = sqlalchemy.Sequence(seqName)
        #return tables
        if isinstance(name, basestring):
            return info[0]
        return info

    def objectsFind(self, domain, objType, filterobject, viewToReturn=None):
        """
        returns a list of matching guids according to the supplied filterobject filters

        @param domain : domain where the objects live
        @param objType : type of object to search
        @param filterobject : a list of filters indicating the view and field-value to use to filter
        @param viewToReturn : the view to use to return the list of found objects
        """
        if viewToReturn:
            table_name = viewToReturn
        else:
            table_name = objType

        # Step 1: turn the filters into a more sane datastructure
        filters = set()
        for filter_ in filterobject.filters:
            view = filter_.keys()[0]
            field = filter_[view].keys()[0]
            value, exact = filter_[view][field]

            filters.add((view, field, value, exact, ))

        filters = tuple(filters)

        # Step 2: Create list of values to retrieve
        table = self.findTable(domain, table_name)
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
            set(self.findTable(domain, filter_[0]) for filter_ in filters if filter_[0] != table_name),
            table)

        # Step 4: Create 'where' clause
        def create_clause((view, field,value, exact, )):
            table = self.findTable(domain, view)
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

        result = None
        # Step 4: Set up basic select query
        query = sqlalchemy.sql.select(fields, where_clause, from_obj=from_obj)
        try:
            result = self.runSqlAlchemyQuery(query)
            if not viewToReturn:
                return tuple(row['guid'] for row in result)
            else:
                rows = tuple(tuple(row.values()) for row in result)
                return coldefs, rows
        finally:
            if result:
                result.close()

    def runSqlAlchemyQuery(self, *args, **kwargs):
        result = None
        try:
            result = self._sqlalchemy_engine.execute(*args, **kwargs)
        except sqlalchemy.exc.DBAPIError, e:
            if not e.connection_invalidated:
                raise
            self._sqlalchemy_engine.dispose()
            result = self._sqlalchemy_engine.execute(*args, **kwargs)
        return result

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
            return OsisView(domain, objType, self._getTableName(domain, viewName), self._getSchemeName(domain, objType))
        else:
            q.eventhandler.raiseCriticalError('[%s] already has a view [%s].'%(objType, viewName))

    def viewAdd(self, view):
        """
        Adds the new view to the database

        @param view : Osisview object to create on the database
        """
        table = view.buildTable(self._sqlalchemy_metadata)
        if not table.exists(self._sqlalchemy_engine):
            table.create(self._sqlalchemy_engine)
        else:
            q.logger.log("View %s already exists in domain %s" % (view.name, view.domain), 4)

    def viewDestroy(self, domain, objType, viewName):
        """
        Removes a view from the database

        @param domain : the object Type's domain
        @param objType : the type of object to destroy
        @param viewName : Osisview object to destroy
        """

        if not self.viewExists(domain, objType, viewName):
            q.eventhandler.raiseCriticalError('%s not found.' % self._getTableName(domain, viewName))
            return

        table = self.findTable(domain, viewName)
        self.runSqlAlchemyQuery(table.drop(cascade=True))
        return True

    def viewDelete(self, domain, objType, viewName, guid, versionguid=None): #pylint: disable=W0613
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

        table = self.findTable(domain, viewName)

        self.runSqlAlchemyQuery(table.delete().where(table.c.guid == guid))
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
        newViewGuid = q.base.idgenerator.generateGUID() #pylint: disable=E1101
        if not isinstance(fields, list):
            fields = [fields,]

        # Add new entry
        table = self.findTable(domain, viewName)

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
                result = self.runSqlAlchemyQuery(query, field)
            finally:
                if result:
                    result.close()

    def _executeQuery(self, query, getdict=True, *args, **kwargs):
        '''
        Execute query and fetch the result in dictformat if getdict is given
        This method uses sqlalchemy to execute queries returning in PyMonkeyDB format
        '''
        result = None
        try:
            with self._lock:
                result = self.runSqlAlchemyQuery(query, *args, **kwargs)
            if getdict and result and not result.closed:

                data = result.fetchall()
                keys = result.keys()
                dictresult = list()
                for row in data:
                    column = dict()
                    for columnname, columndata in itertools.izip(keys, row):
                        if isinstance(columndata, datetime.datetime):
                            columndata = str(columndata)
                        column[columnname] = columndata
                    dictresult.append(column)
                return dictresult
        finally:
            if result:
                result.close()
        return list()

    def _createObject(self, domain, data):
        """
        Store the supplied data in the database
        @param data : object to store
        """

        tableName = data.__class__.__name__ + "_obj"
        table = self.findTable(domain, tableName)

        obj = ThriftSerializer.serialize(data)
        if data.creationdate:
            creationdate = float(data.creationdate)
            creationdate = datetime.datetime.fromtimestamp(creationdate)
        else:
            creationdate = None

        insert = table.insert().values(guid=data.guid, creationdate=creationdate, data=obj)

        try:
            self.runSqlAlchemyQuery(insert).close()
        except ProgrammingError, ex:
            raise OsisException(str(insert), ex)
        return data

    def _updateObject(self, domain, data):
        """
        Update the supplied data in the database

        @param data : object to update
        """

        tableName = data.__class__.__name__ + "_obj"
        table = self.findTable(domain, tableName)

        obj = ThriftSerializer.serialize(data)

        update = table.update().where(table.c.guid == data.guid).values(data=obj)

        try:
            self.runSqlAlchemyQuery(update).close()
        except ProgrammingError, ex:
            raise OsisException(str(update), ex)
        return data

    def objectSave(self, domain, data):
        """
        Update or create the supplied object

        @param objType : type of object to check
        @param guid : unique identifier
        """
        if not self.objectExists(domain, data.__class__.__name__, data.guid):
            return self._createObject(domain, data)
        else:
            return self._updateObject(domain, data)

    def objectGet(self, domain, objType, guid):
        """
        Get an instance of objType with the supplied guid

        @param objType : type of object to check
        @param guid : unique identifier
        """

        tableName = objType + "_obj"
        table = self.findTable(domain, tableName)

        select = sqlalchemy.sql.select([ table.c.data ], table.c.guid == guid)
        errorStr = '%s.%s with guid %s not found.' % (domain, objType, guid)

        result = self.runSqlAlchemyQuery(select)
        if not result:
            q.eventhandler.raiseCriticalError(errorStr)
        else:
            retval = result.fetchone()
            if not retval:
                q.eventhandler.raiseCriticalError(errorStr)
            else:
                result.close()
                return retval[0]

    def objectDelete(self, domain, objType, guid):
        """
        Delete an instance of objType with the supplied guid

        @param objType : type of object to check
        @param guid : unique identifier
        """

        if self.objectExists(domain, objType, guid):
            tableName = objType + "_obj"
            table = self.findTable(domain, tableName)

            delete = table.delete().where(table.c.guid == guid)

            self.runSqlAlchemyQuery(delete).close()
            return True
        else:
            q.eventhandler.raiseCriticalError('%s.%s with guid %s not found.' % (domain, objType, guid))

    def objectExists(self, domain, objType, guid):
        """
        Checks if an instance of objType with the supplied guid exists

        @param objType : type of object to check
        @param guid : unique identifier
        """

        tableName = objType + "_obj"
        table = self.findTable(domain, tableName)

        select = sqlalchemy.sql.select([ table.c.guid ], table.c.guid == guid)

        result = self.runSqlAlchemyQuery(select)
        if result:
            retval = result.fetchone()
            if retval:
                return True
        return False
