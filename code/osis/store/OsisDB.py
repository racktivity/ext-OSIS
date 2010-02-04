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

from pymonkey import q
from pymonkey.baseclasses.ManagementApplication import ManagementApplication
from pymonkey.db.DBConnection import DBConnection
from OsisConnection import OsisConnection

class OsisDB(object):
    
    """
    Borg singleton OsisDB object
    """
    _we_are_one = {}

    def __init__(self):
        #implement the borg pattern (we are one)
        self.__dict__ = self._we_are_one


    def addConnection(self, name,
            jdbip, jdbnamespace, jdblogin, jdbpasswd, jdbmaster='', jdbport=2181,
            pgsip="127.0.0.1", pgsdatabase=None, pgslogin=None, pgspasswd=None ):
        """
        Add an Osis connection to the configuration

        @param name : connection name
        @param ip : ip address for the database server
        @param database : name of the database to connect to
        @param login : login for the db server
        @param passwd : password for the db server
        """

        if not pgsdatabase: pgsdatabase = jdbnamespace
        if not pgslogin: pgslogin = jdblogin
        if not pgspasswd: pgspasswd = jdbpasswd

        iniFile = q.system.fs.joinPaths(q.dirs.cfgDir, 'osisdb.cfg')
        if not q.system.fs.exists(iniFile):
            ini = q.tools.inifile.new(iniFile)
        else:
            ini = q.tools.inifile.open(iniFile)

        if not ini.checkSection(name):
            ini.addSection(name)

        ini.addParam(name,'ip', jdbip)
        ini.addParam(name,'database', jdbnamespace)
        ini.addParam(name,'login', jdblogin)
        ini.addParam(name,'passwd', jdbpasswd)
        ini.addParam(name,'master', jdbmaster)
        ini.addParam(name,'port', jdbport)

        ini.addParam(name,'pgsip', pgsip)
        ini.addParam(name,'pgsdatabase', pgsdatabase)
        ini.addParam(name,'pgslogin', pgslogin)
        ini.addParam(name,'pgspasswd', pgspasswd)

        ini.write()


    def removeConnection(self, name):
        """
        Remove an Osis connection from the configuration

        @param name : connection name
        """
        iniFile = q.system.fs.joinPaths(q.dirs.cfgDir, 'osisdb.cfg')
        if not q.system.fs.exists(iniFile):
            q.logger.log("config file not found",3)
        else:
            ini = q.tools.inifile.open(iniFile)

            if not ini.checkSection(name):
                q.logger.log("config file not found",3)
            else:
                ini.removeSection(name)

    def listConnections(self):
        """
        List all connections
        """
        iniFile = q.system.fs.joinPaths(q.dirs.cfgDir, 'osisdb.cfg')
        connections = list()
        if q.system.fs.exists(iniFile):
            ini = q.tools.inifile.open(iniFile)
            connections = ini.getSections()
        return connections

    def getConnection(self, name):
        """
        Create an Osis connection

        @param name : connection name
        """
        # Initialize connections if not available
        if not hasattr(self, '_connections'):
            q.logger.log('>>> Initializing connections', 8)
            self._connections = {}
            
        # Use existing connection if available
        if name in self._connections:
            q.logger.log('>>> Reusing connection %s' % name, 8)
            return self._connections[name]
        
            
        
        osisConn = OsisConnection()
        iniFile = q.system.fs.joinPaths(q.dirs.cfgDir, 'osisdb.cfg')
        if not q.system.fs.exists(iniFile):
            q.logger.log("config file not found",3)
            q.eventhandler.raiseCriticalError('Configuration file not found. Please configure the connection.')
        else:
            ini = q.tools.inifile.open(iniFile)

        ip = ini.getValue(name,'ip')
        namespace = ini.getValue(name,'database')
        login = ini.getValue(name,'login')
        passwd = ini.getValue(name,'passwd')
        master = ini.getValue(name,'master')
        port = ini.getValue(name,'port')

        try:
            pgsip = ini.getValue(name,'pgsip')
        except:
            pgsip = "127.0.0.1"

        try:
            pgsdatabase = ini.getValue(name,'pgsdatabase')
        except:
            pgsdatabase = namespace

        try:
            pgslogin = ini.getValue(name,'pgslogin')
        except:
            pgslogin = login

        try:
            pgspasswd = ini.getValue(name,'pgspasswd')
        except:
            pgspasswd = passwd
        
        osisConn.connect(ip, namespace, login, passwd, master, port,
                        pgsip, pgsdatabase, pgslogin, pgspasswd)
        
        # Cache connection
        q.logger.log('>>> Caching connection %s' % name, 8)
        self._connections[name] = osisConn
        
        return osisConn

