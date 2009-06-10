class Cloudcentral_acl(CloudApiBase):

    @q.manage.applicationserver.expose_authenticated
    def createUser(self, login, password, description, applicationserver_request=None):
        """
        Create a new user

        @param login: Login of user
        @type login: string
        @param password: Password of user
        @type password: string
        @param description: Description of user
        @type description: string
        @return: guid #Global unique identifier of this user
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def removeUser(self, login, applicationserver_request=None):
        """
        Remove the user specified

        @param login: Login of user
        @type login: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def createGroup(self, name, description, applicationserver_request=None):
        """
        Create a new group

        @param name: Name of group
        @type name: string
        @param description: Description of group
        @type description: string
        @return: guid #Global unique identifier of this group
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def removeGroup(self, name, applicationserver_request=None):
        """
        Remove the group specified

        @param name: Name of group
        @type name: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def addUserToGroup(self, login, group, applicationserver_request=None):
        """
        Add the user to the group specified

        @param login: Login of user
        @type login: string
        @param group: Name of group
        @type group: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def removeUserFromGroup(self, login, group, applicationserver_request=None):
        """
        Remove the user from the group specified

        @param login: Login of user
        @type login: string
        @param group: Name of group
        @type group: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def listPermissions(self, applicationserver_request=None):
        """
        List all known permissions

        @return: list of rights (Read, Write, Execute, ...)
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def grantUserPermissionToMachine(self, machine, login, permission, applicationserver_request=None):
        """
        Grant user permission

        @param machine: Global unique identifier of machine
        @type machine: guid
        @param login: Login of user
        @type login: string
        @param permission: Type of permission (Read, Write, Execute, ...)
        @type permission: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def revokeUserPermissionToMachine(self, machine, login, permission, applicationserver_request=None):
        """
        Revoke user permission

        @param machine: Global unique identifier of machine
        @type machine: guid
        @param login: Login of user
        @type login: string
        @param permission: Type of permission (Read, Write, Execute, ...)
        @type permission: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def grantGroupPermissionToMachine(self, machine, group, permission, applicationserver_request=None):
        """
        Grant group permission

        @param machine: Global unique identifier of machine
        @type machine: guid
        @param group: Name of group
        @type group: string
        @param permission: Type of permission (Read, Write, Execute, ...)
        @type permission: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def revokeGroupPermissionToMachine(self, machine, group, permission, applicationserver_request=None):
        """
        Revoke group permission

        @param machine: Global unique identifier of machine
        @type machine: guid
        @param group: Name of group
        @type group: string
        @param permission: Type of permission (Read, Write, Execute, ...)
        @type permission: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def grantUserPermissionToUser(self, login, logingranted, permission, applicationserver_request=None):
        """
        Grant user permission

        @param login: Login of user
        @type login: string
        @param logingranted: Login of the user who is granted access
        @type logingranted: string
        @param permission: Type of permission (Read, Write, Execute, ...)
        @type permission: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def revokeUserPermissionToUser(self, login, loginrevoked, permission, applicationserver_request=None):
        """
        Revoke user permission

        @param login: Login of user
        @type login: string
        @param loginrevoked: Login of the user who is revoked access
        @type loginrevoked: string
        @param permission: Type of permission (Read, Write, Execute, ...)
        @type permission: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def grantGroupPermissionToUser(self, login, group, permission, applicationserver_request=None):
        """
        Grant group permission

        @param login: Login of user
        @type login: string
        @param group: Name of group
        @type group: string
        @param permission: Type of permission (Read, Write, Execute, ...)
        @type permission: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def revokeGroupPermissionToUser(self, login, group, permission, applicationserver_request=None):
        """
        Revoke group permission

        @param login: Login of user
        @type login: string
        @param group: Name of group
        @type group: string
        @param permission: Type of permission (Read, Write, Execute, ...)
        @type permission: string
        @return: True or Error
        """
        pass #TODO


class Cloudcentral_machines(CloudApiBase):

    @q.manage.applicationserver.expose_authenticated
    def listMachineTypes(self, applicationserver_request=None):
        """
        List of all possible machine types

        @return: list of machine types
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def listIpAddressTypes(self, applicationserver_request=None):
        """
        List of all possible IP address types

        @return: list of IP address types
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def addBoxOffice(self, zenithid, applicationserver_request=None):
        """
        Add a new BoxOffice environment

        @param zenithid: Zenith's unique idenfifier
        @type zenithid: string
        @return: guid # Global unique identifier for this BoxOffice environment
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def removeBoxOffice(self, zenithid, applicationserver_request=None):
        """
        Remove this BoxOffice environment

        @param zenithid: Zenith's unique idenfifier
        @type zenithid: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def addMachine(self, boxoffice, zenithid, name, type, ipaddresses, applicationserver_request=None):
        """
        Add a machine to a BoxOffice environment

        @param boxoffice: Global unique identifier of a BoxOffice environment
        @type boxoffice: guid
        @param zenithid: Zenith's unique idenfifier
        @type zenithid: string
        @param type: Type of machine
        @type type: string
        @param ipaddresses: List of tuples holding IP address and type
        @type ipaddresses: list
        @return: guid # Global unique idenfifier for this BoxOffice environment
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def removeMachine(self, boxoffice, zenithid, applicationserver_request=None):
        """
        Remove a machine from a BoxOffice environment

        @param boxoffice: Global unique identifier of a BoxOffice environment
        @type boxoffice: guid
        @param zenithid: Zenith's unique idenfifier
        @type zenithid: string
        @return: True or Error
        """
        pass #TODO