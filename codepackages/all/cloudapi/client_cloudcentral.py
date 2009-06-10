class CloudApiClient:
    def __init__(self, proxy):
        self._proxy = proxy


class Cloudcentral_acl(CloudApiClient):
    def createUser(self, login, password, description):
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
        return self._proxy.cloud_api_cloudcentral_acl.createUser(login, password, description)

    def removeUser(self, login):
        """
        Remove the user specified

        @param login: Login of user
        @type login: string
        @return: True or Error
        """
        return self._proxy.cloud_api_cloudcentral_acl.removeUser(login)

    def createGroup(self, name, description):
        """
        Create a new group

        @param name: Name of group
        @type name: string
        @param description: Description of group
        @type description: string
        @return: guid #Global unique identifier of this group
        """
        return self._proxy.cloud_api_cloudcentral_acl.createGroup(name, description)

    def removeGroup(self, name):
        """
        Remove the group specified

        @param name: Name of group
        @type name: string
        @return: True or Error
        """
        return self._proxy.cloud_api_cloudcentral_acl.removeGroup(name)

    def addUserToGroup(self, login, group):
        """
        Add the user to the group specified

        @param login: Login of user
        @type login: string
        @param group: Name of group
        @type group: string
        @return: True or Error
        """
        return self._proxy.cloud_api_cloudcentral_acl.addUserToGroup(login, group)

    def removeUserFromGroup(self, login, group):
        """
        Remove the user from the group specified

        @param login: Login of user
        @type login: string
        @param group: Name of group
        @type group: string
        @return: True or Error
        """
        return self._proxy.cloud_api_cloudcentral_acl.removeUserFromGroup(login, group)

    def listPermissions(self):
        """
        List all known permissions

        @return: list of rights (Read, Write, Execute, ...)
        """
        return self._proxy.cloud_api_cloudcentral_acl.listPermissions()

    def grantUserPermissionToMachine(self, machine, login, permission):
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
        return self._proxy.cloud_api_cloudcentral_acl.grantUserPermissionToMachine(machine, login, permission)

    def revokeUserPermissionToMachine(self, machine, login, permission):
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
        return self._proxy.cloud_api_cloudcentral_acl.revokeUserPermissionToMachine(machine, login, permission)

    def grantGroupPermissionToMachine(self, machine, group, permission):
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
        return self._proxy.cloud_api_cloudcentral_acl.grantGroupPermissionToMachine(machine, group, permission)

    def revokeGroupPermissionToMachine(self, machine, group, permission):
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
        return self._proxy.cloud_api_cloudcentral_acl.revokeGroupPermissionToMachine(machine, group, permission)

    def grantUserPermissionToUser(self, login, logingranted, permission):
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
        return self._proxy.cloud_api_cloudcentral_acl.grantUserPermissionToUser(login, logingranted, permission)

    def revokeUserPermissionToUser(self, login, loginrevoked, permission):
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
        return self._proxy.cloud_api_cloudcentral_acl.revokeUserPermissionToUser(login, loginrevoked, permission)

    def grantGroupPermissionToUser(self, login, group, permission):
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
        return self._proxy.cloud_api_cloudcentral_acl.grantGroupPermissionToUser(login, group, permission)

    def revokeGroupPermissionToUser(self, login, group, permission):
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
        return self._proxy.cloud_api_cloudcentral_acl.revokeGroupPermissionToUser(login, group, permission)


class Cloudcentral_machines(CloudApiClient):
    def listMachineTypes(self):
        """
        List of all possible machine types

        @return: list of machine types
        """
        return self._proxy.cloud_api_cloudcentral_machines.listMachineTypes()

    def listIpAddressTypes(self):
        """
        List of all possible IP address types

        @return: list of IP address types
        """
        return self._proxy.cloud_api_cloudcentral_machines.listIpAddressTypes()

    def addBoxOffice(self, zenithid):
        """
        Add a new BoxOffice environment

        @param zenithid: Zenith's unique idenfifier
        @type zenithid: string
        @return: guid # Global unique identifier for this BoxOffice environment
        """
        return self._proxy.cloud_api_cloudcentral_machines.addBoxOffice(zenithid)

    def removeBoxOffice(self, zenithid):
        """
        Remove this BoxOffice environment

        @param zenithid: Zenith's unique idenfifier
        @type zenithid: string
        @return: True or Error
        """
        return self._proxy.cloud_api_cloudcentral_machines.removeBoxOffice(zenithid)

    def addMachine(self, boxoffice, zenithid, name, type, ipaddresses):
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
        return self._proxy.cloud_api_cloudcentral_machines.addMachine(boxoffice, zenithid, name, type, ipaddresses)

    def removeMachine(self, boxoffice, zenithid):
        """
        Remove a machine from a BoxOffice environment

        @param boxoffice: Global unique identifier of a BoxOffice environment
        @type boxoffice: guid
        @param zenithid: Zenith's unique idenfifier
        @type zenithid: string
        @return: True or Error
        """
        return self._proxy.cloud_api_cloudcentral_machines.removeMachine(boxoffice, zenithid)