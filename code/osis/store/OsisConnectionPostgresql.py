from pylabs import q
from OsisConnection import OsisConnection

class OsisConnectionPostgresql(OsisConnection):
    def __init__(self, dbtype, sequences = None):
        super(OsisConnectionPostgresql, self).__init__(dbtype, sequences)

    def _getTableName(self, domain, objType):
        """
        Get the table name

        @param domain : name of the domain
        @param objType : name of the object type
        """
        return objType

    def _getSchemeName(self, domain, objType):
        """
        Get the scheme name

        @param domain : name of the domain
        @param objType : name of the object type
        """
        return domain

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

        sql = 'CREATE SCHEMA %s' % schema
        self._executeQuery(sql, False)

    def schemeExists(self, domain, name):
        """
        Checks if the schema with the supplied name exists

        @param domain : domain to check for the schema
        @param name : name of the schema to check
        """
        schema = self._getSchemeName(domain, name)

        sql =  "SELECT schema_name FROM information_schema.schemata WHERE schema_name = '%s'" % schema
        result = self._executeQuery(sql)

        if result:
            return True
        else:
            return False
