from OsisConnection import OsisConnection

class OsisConnectionOracle(OsisConnection):
    def __init__(self, dbtype):
        super(OsisConnectionOracle, self).__init__(dbtype)

    def _getTableName(self, domain, objType):
        """
        Get the table name

        @param domain : name of the domain
        @param objType : name of the object type
        """
        return "%s_%s" % (domain, objType)

    def _getSchemeName(self, domain, objType):
        """
        Get the scheme name

        @param domain : name of the domain
        @param objType : name of the object type
        """

        # We don't use schemas
        return self._sqlalchemy_engine.url.username

    def schemeCreate(self, domain, name):
        """
        Creates the model structure on the database

        @param domain : domain to create the scheme in
        @param objTypeName : the name of the type to create
        """

        # We don't use schemas so don't do anything
        pass

    def schemeExists(self, domain, name):
        """
        Checks if the schema with the supplied name exists

        @param domain : domain to check for the schema
        @param name : name of the schema to check
        """

        # We don't use schemas so don't do anything
        return True
