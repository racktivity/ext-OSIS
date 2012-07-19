from pylabs import q
from OsisConnectionPostgresql import OsisConnectionPostgresql
from OsisConnectionOracle import OsisConnectionOracle

class OsisConnectionFactory(object):
    def __init__(self):
        raise NotImplementedError()

    @staticmethod
    def create(dbtype='postgresql'):
        className = None
        if dbtype == "postgresql":
            className = OsisConnectionPostgresql
        elif dbtype == "oracle":
            className = OsisConnectionOracle
        else:
            q.eventhandler.raiseCriticalError("Failed to load OsisConnection for database type %s" % dbtype)
            return None
        return className(dbtype)
