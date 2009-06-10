class Machine(CloudApiBase):

    @q.manage.applicationserver.expose_authenticated
    def createByIP(self, vpdc, name, templateName, description, ipAddresses, capacityProperties, properties, applicationserver_request=None):
        """
        Create a machine starting from a simple set of parameters. This method uses IP addresses as input

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param name: Name of the machine. The name is a freely chosen name, which has to be unique in SPACE
        @type name: string
        @param templateName: Name of a machine template, which must exist in the Space. To obtain the list of available
                             machine templates, run machinetemplate.list()
        @type templateName: string
        @param description: This is free text describing the purpose of the machine, if multi-line use back-slash + n
        @type description: string
        @param ipAddresses: Is a list of IP addresses which will be given to a machine. The CloudAPI checks if these IP
                            addresses exist on Public Networks or Private Networks which belong to the customer, if not
                            an error is thrown
        @type ipAddresses: list(string)
        @param capacityProperties: The keys of the dict are the names of capacity properties, the values of the dict
                                   must be possible values for the capacity property.
                                   Example: {"Machine Performance": "200MB RAM + 800Mhz CPU", "Data Disk": "10GB"}
                                   If you want to know the possible names/values, run machinetemplate.list() and
                                   machinetemplate.getDetails(templateName).
        @type capacityProperties: dict
        @param properties: This is a dict of property/value pairs as part of the capacityProperties dict. The parameter
                           names must be existing properties for the chosen machine template,
                           If you want to know the possibilities, see machinetemplate.list() and
                           machinetemplate.getDetails(templateName).
        @type properties: dict
        @return: Machine name
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def createByNetwork(self, vpdc, name, templateName, description, publicIPRange, privateNetworks, capacityProperties, properties, applicationserver_request=None):
        """
        Create a machine starting from a simple set of parameters. This method uses predefined network names as input.
        The IP addresses are chosen automatically.

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param name: Name of the machine. The name is a freely chosen name, which has to be unique in SPACE
        @type name: string
        @param templateName: Name of a machine template, which must exist in the Space. To obtain the list of available
                             machine templates, run machinetemplate.list()
        @type templateName: string
        @param description: This is free text describing the purpose of the machine, if multi-line use back-slash + n
        @type description: string
        @param publicIPRange: The name of an existing publicIPRange. The CloudAPI will check if there are IP addresses
                              available on the defined IPRANGE, if not an error is thrown. One IP address will be given.
                              To know the list of network names, use: publiciprange.list()
                              If you want to know if there are free IP addresses, use publiciprange.listFreeIP() .
                              If you do not specify this parameter (""), the machine will not be connected to a public
                              network.
        @type publicIPRange: string
        @param privateNetworks: Is a list of private networks names. The machine will be connected to one of these
                                private networks upon the deployment of the machine. An error will be thrown if the
                                private networks don't exist in the space, or if there are no IP addresses available on
                                the private network.
                                If one or more private networks do not belong to the VPDC, they will be added
                                automatically.
                                The machine will get one IP address from each private network.
                                To know which network names do exist use: privatenetwork.list().  To know the free IP
                                addresses, use privatenetwork.listFreeIP().
                                If the private network does not exist in the VPDC, the CloudAPI links it to the VPDC
                                automatically. The first Public Network will be assigned to the Pubic Network object
                                that is present in the VPDC by default. For additional Public Networks, objects will be
                                created automatically.
        @type privateNetworks: list(string)
        @param capacityProperties: The keys of the dict are the names of capacity properties, the values of the dict
                                   must be possible values for the capacity property.
                                   Example: {"Machine Performance": "200MB RAM + 800Mhz CPU", "Data Disk": "10GB"}
                                   If you want to know the possible names/values, run machinetemplate.list() and
                                   machinetemplate.getDetails(templateName).
        @type capacityProperties: dict
        @param properties: This is a dict of property/value pairs as part of the capacityProperties dict. The parameter
                           names must be existing properties for the chosen machine template,
                           If you want to know the possibilities, see machinetemplate.list() and
                           machinetemplate.getDetails(templateName).
        @type properties: dict
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def ipAddressAdd(self, vpdc, machine, ipAddress, applicationserver_request=None):
        """
        A new IP address and/or private or public LAN will be added to an existing virtual machine. If required a new
        Private LAN or Public LAN  will be attached to the machine (Only implemented for public IP addresses now)

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine
        @type machine: string
        @param ipAddress: IP address to be added to the machine. The CloudAPI checks if this IP address exists in a
                          private or publick network. Use privatenetwork.listFreeIP() or
                          publiciprange.listFreeIPFromIPRange() to check which IP addresses can be used
        @type ipAddress: string
        @return: string with IP address
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def ipAddressDelete(self, vpdc, machine, ipAddress, applicationserver_request=None):
        """
        Delete an IP address from a machine

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine
        @type machine: string
        @param ipAddress: IP address to be removed from the machine. Use machine.getMachineDetails(vpdc, machine) to
                          know the IP addresses of the machine.
        @type ipAddress: string
        @return: string with IP address
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def delete(self, vpdc, machine, applicationserver_request=None):
        """
        Remove a machine from a VPDC, but keep the machine in the model.

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine
        @type machine: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def rename(self, vpdc, oldName, newName, applicationserver_request=None):
        """
        Rename a machine in a VPDC

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param oldName: The current name of the machine
        @type oldName: string
        @param newName: The new name of the machine
        @type newName: string
        @return: New name of the machine
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def setDescription(self, vpdc, machine, description, applicationserver_request=None):
        """
        Set a description on a machine

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine
        @type machine: string
        @param description: New description of the machine
        @type description: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def list(self, vpdc, applicationserver_request=None):
        """
        list machines in a VPDC

        @param vpdc: Name of VPDC
        @type vpdc: string
        @return: [], list of machine names
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def start(self, vpdc, machine, applicationserver_request=None):
        """
        Start a machine (if machine is hibernated use machine.resume())

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine
        @type machine: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def stop(self, vpdc, machine, applicationserver_request=None):
        """
        Shut down a machine

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine
        @type machine: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def reboot(self, vpdc, machine, applicationserver_request=None):
        """
        Reboot a machine

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine
        @type machine: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def backup(self, vpdc, machine, applicationserver_request=None):
        """
        Create a backup of a machine

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine
        @type machine: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def listBackups(self, vpdc, machine, applicationserver_request=None):
        """
        List with all the backups of a machine

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine
        @type machine: string
        @return: [], list with the names of the backups of the machine
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def restoreBackup(self, vpdc, machine, backup, applicationserver_request=None):
        """
        Restore a backup and remove the current machine state

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine
        @type machine: string
        @param backup: Name of the backup to restore
        @type backup: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def exportBackup(self, vpdc, machine, backup, target, targetLogin, targetPassword, applicationserver_request=None):
        """
        Export a backup to a remote location

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine
        @type machine: string
        @param backup: Name of the backup to export
        @type backup: string
        @param target: Location where the backup should be saved
        @type target: string
        @param targetLogin: Login to access the remote target
        @type targetLogin: string
        @param targetPassword: Password linked to the login, to allow  access to the target location
        @type targetPassword: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def listCapacityProperties(self, vpdc, machine, applicationserver_request=None):
        """
        List all Capacity Properties and their corresponding values on a machine

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine
        @type machine: string
        @return: dict, "capacityProperty: string"
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def listProperties(self, vpdc, machine, applicationserver_request=None):
        """
        List of all properties of a machine and their corresponding values

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine
        @type machine: string
        @return: dict, "property: string"
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def setCapacityProperty(self, vpdc, machine, capacityproperty, value, applicationserver_request=None):
        """
        Set a value for a capacity property on a machine

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine
        @type machine: string
        @param capacityproperty: Name of the capacity property
        @type capacityproperty: string
        @param value: Value for the capacity property
        @type value: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def setProperty(self, vpdc, machine, property, value, applicationserver_request=None):
        """
        Set a value for a property on a machine

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine
        @type machine: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def getMachineDetails(self, vpdc, machine, applicationserver_request=None):
        """
        Get the details of a machine, such as machine name, status, memory, CPU, ...

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine
        @type machine: string
        @return: { name: <string>, runStatus: <string>, modelStatus: <string>, description: <string>, hostname:
                 <string>, os: <string>, cpu: <int>, memory: <int>,
                 networkinterfaces:  [ { nic: <string>, macaddress: <string>, ipaddress: <string>, netmask: <string>,
                 gateway: <string> } , ... ],
                 backups:            [ { name: <string>, type: <string>, created: <datetime> } , ... ],
                 services:           [ { application: <string>, enabled: <boolean>, login: <string> } , ... ],
                 capacityProperties: { propertyName(string): value(string), ...},
                 properties:         { propertyName(string): value(string), ...}
                 }
                 The runsStatus-string is one of the DRP Machine statuses. ("halted", "running", "paused", ...), the
                 modelStatus-string is one of the vpdcObjectStatuses ("deployed", "error", ...)
                 CPU is in Mhz, memory is in MB RAM.
                 Newlines in the description are encoded as backslash-n.
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def executeQshellScript(self, vpdc, machine, qshellScriptContent, applicationserver_request=None):
        """
        Execute a Q-Shell script on a machine. This function requires a Q-Agent on the machine

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine
        @type machine: string
        @return: dict, {"jobGuid: string,status:string}
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def copyFromTemplate(self, sourcevpdc, targetvpdc, machine, nameOfCopy, applicationserver_request=None):
        """
        Copy a machine, independent if the machine is deployed or not. The disks will have the original
        template-content, but the CapacityProperties and Properties are copied to the new machine.
        The copied machine is automatically connected to the same public and private networks as the original machine,
        with an arbitrary IP address. If one of the connected networks has insufficient free IP addresses, an error is
        thrown.

        @param sourcevpdc: Name of the VPDC (Virtual Data Center) from which we want to copy a machine
        @type sourcevpdc: string
        @param targetvpdc: Name of the VPDC (Virtual Data Center) in which we want to create a machine
        @type targetvpdc: string
        @param machine: Name of the machine
        @type machine: string
        @param nameOfCopy: New name for the created copy
        @type nameOfCopy: string
        @return: True or Error
        """
        pass #TODO


class Publiciprange(CloudApiBase):

    @q.manage.applicationserver.expose_authenticated
    def list(self, applicationserver_request=None):
        """
        List of all public IP ranges

        @return: dict, {publicIPRangeName:"StartIPAddress-StopIPAddress",...}
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def listInVpdc(self, vpdc, applicationserver_request=None):
        """
        List of all public IP ranges in a VPDC

        @param vpdc: Name of VPDC
        @type vpdc: string
        @return: dict, {publicIPRangeName:"StartIPAddress-StopIPAddress",...}
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def listWithFreeIPAddresses(self, applicationserver_request=None):
        """
        List of all public IP ranges which have one or more free IP addresses

        @return: dict, The keys are the names of the public IP ranges, the values are lists of free IP Addresses.
                 Public IP ranges without free addresses are not included. (So an empty list will never appear as
                 value.)
                 Example: {publicipRangeName, ["1.2.3.4", "1.2.3.6"],...}
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def listFreeIPFromIPRange(self, name, applicationserver_request=None):
        """
        List of free IP addresses in a public IP range. If the name is empty, you get the free IP addresses of all
        public IP ranges

        @param name: Name of a public IP range. The name is unique within space
        @type name: string
        @return: [], list of free IP addresses
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def rename(self, oldName, newName, applicationserver_request=None):
        """
        Rename a public IP range, the original name is given by the cloud provider, the cloud user can change it.

        @param oldName: Name of the public IP range, given by the cloud provider
        @type oldName: string
        @param newName: New name of the public IP range
        @type newName: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def getDetails(self, name, applicationserver_request=None):
        """
        Get the details of a public IP range

        @param name: Name of a public IP range. The name is unique within space
        @type name: string
        @return: dict, {name: string, customer: string, network: string, netmask: string,startiprange:
                 string,stopiprange: string,gateway: string, domainnameservers: string}
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def split(self, name, newIpRangeName, nrOfIps, applicationserver_request=None):
        """
        Split an existing IP range into subranges. The original IP ranges are given by the cloud provider.

        @param name: Name of a public IP range. The name is unique within space
        @type name: string
        @param newIpRangeName: Name of new public IP range
        @type newIpRangeName: string
        @param nrOfIps: Number of IP addresses for the new IP range
        @type nrOfIps: integer
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def delete(self, name, applicationserver_request=None):
        """
        Delete a public IP range

        @param name: Name of a public IP range. The name is unique within space
        @type name: string
        @return: True or Error
        """
        pass #TODO


class Privatenetwork(CloudApiBase):

    @q.manage.applicationserver.expose_authenticated
    def list(self, applicationserver_request=None):
        """
        List of all private networks

        @return: array(dict)  [{privateNetworkName:name, network:aipaddr, subnet:mask}]
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def listInVpdc(self, vpdc, applicationserver_request=None):
        """
        List of all private networks in a VPDC

        @param vpdc: Name of VPDC
        @type vpdc: string
        @return: array(dict)  [{privateNetworkName:name, network:aipaddr, subnet:mask}]
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def rename(self, oldName, newName, applicationserver_request=None):
        """
        Rename a private network, the original name is automatically created when a private network is needed

        @param oldName: Name of the public IP range, given by the cloud provider
        @type oldName: string
        @param newName: New name of the public IP range
        @type newName: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def listFreeIP(self, name, applicationserver_request=None):
        """
        List of free IP addresses in a private network. A name of the private network must be provided with this
        function

        @param name: Name of a public IP range. The name is unique within space
        @type name: string
        @return: [], list of free IP addresses
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def create(self, name, applicationserver_request=None):
        """
        Create a new private network. The cloud software will make sure a new VLAN (or comparable technology) is created
        with a unique name in the cloud domain.

        @param name: Name of a public IP range. The name is unique within space
        @type name: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def getDetails(self, name, applicationserver_request=None):
        """
        Get the details of a private network

        @param name: Name of a public IP range. The name is unique within space
        @type name: string
        @return: {}, {name: string, customer: string, network: string, netmask: string,gateway: string,
                 domainnameservers: string}
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def delete(self, name, applicationserver_request=None):
        """
        Delete a private network if no machine is using it. An error is thrown if a machine uses the private network

        @param name: Name of a public IP range. The name is unique within space
        @type name: string
        @return: True or Error
        """
        pass #TODO


class Machinetemplate(CloudApiBase):

    @q.manage.applicationserver.expose_authenticated
    def list(self, applicationserver_request=None):
        """
        List of all available machine templates

        @return: tuple of machine template names
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def getDetails(self, machineTemplate, applicationserver_request=None):
        """
        Get the details of a machine template

        @param machineTemplate: Name of the template
        @type machineTemplate: string
        @return: dict, {name:string, description: string, Type: string, OS: string, capacityProperties:
                 {propertyName(string): value(string), ...}, properties: {propertyName(string): value(string), ...},
                 Ports:{portName(string): {Type: string,capacityProperties: {propertyName(string): value(string), ...}},
                 ...}}
        """
        pass #TODO


class Portal(CloudApiBase):

    @q.manage.applicationserver.expose_authenticated
    def getVersion(self, applicationserver_request=None):
        """
        This function is only to check the version of the CloudAPI

        @return: string, Version of the CloudAPI
        """
        pass #TODO


class Vpdc(CloudApiBase):

    @q.manage.applicationserver.expose_authenticated
    def create(self, vpdc, applicationserver_request=None):
        """
        Create a new VPDC, based on a VPDC-template

        @param vpdc: Name of VPDC
        @type vpdc: string
        @return: string, name of the VPDC
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def delete(self, vpdc, applicationserver_request=None):
        """
        Delete a VPDC

        @param vpdc: Name of VPDC
        @type vpdc: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def deploy(self, vpdc, applicationserver_request=None):
        """
        Deploy a VPDC

        @param vpdc: Name of VPDC
        @type vpdc: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def list(self, applicationserver_request=None):
        """
        Get a list of all VPDCs

        @return: tuple of VPDC names
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def start(self, vpdc, applicationserver_request=None):
        """
        Start all machines in a VPDC

        @param vpdc: Name of VPDC
        @type vpdc: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def stop(self, vpdc, applicationserver_request=None):
        """
        Stop all machines in a VPDC

        @param vpdc: Name of VPDC
        @type vpdc: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def getDeployStatus(self, vpdc, applicationserver_request=None):
        """
        Get the deploy-status of the VPDC.
        Mapping of DRP states on CloudAPI states:
        * DRP UNCONFIGURED, CONFIGURED, MODELED  => CloudAPI UNDEPLOYED
        * DRP PROCESSING, DEPLOYING  => CloudAPI DEPLOYING
        * DRP DEPLOYED  => CloudAPI
        DEPLOYED * DRP CHANGED  => CloudAPI CHANGED
        * DRP DELETE, DELETED, DELETING  => CloudAPI UNDEPLOYING
        * DRP ERROR  => CloudAPI ERROR

        @param vpdc: Name of VPDC
        @type vpdc: string
        @return: String: "UNDEPLOYED", "DEPLOYING", "DEPLOYED", "CHANGED", "UNDEPLOYING"or "ERROR"
        """
        pass #TODO


class Subspace(CloudApiBase):

    @q.manage.applicationserver.expose_authenticated
    def create(self, subSpace, processingCredits, storageCredits, networkingCredits, userFirstName, userLastName, userLogin, userPassword, email, applicationserver_request=None):
        """
        Create a new  sub-space

        @param subSpace: Name of the sub-space
        @type subSpace: string
        @param processingCredits: Amount of processing credits, assigned to this space
        @type processingCredits: integer
        @param storageCredits: Amount of storage credits, assigned to this space
        @type storageCredits: integer
        @param networkingCredits: Amount of networking credits, assigned to this space
        @type networkingCredits: integer
        @param userFirstName: First name of the user
        @type userFirstName: string
        @param userLastName: Last name of the user
        @type userLastName: string
        @param userLogin: User login to access the new space
        @type userLogin: string
        @param userPassword: User password to access the new space
        @type userPassword: string
        @param email: E-mail address to reach the customer
        @type email: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def delete(self, subSpace, applicationserver_request=None):
        """
        Delete a sub-space

        @param subSpace: Name of the sub-space
        @type subSpace: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def listSubSpaces(self, applicationserver_request=None):
        """
        List all sub-spaces

        @return: tuple of sub-space names
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def addUser(self, subSpace, userFirstName, userLastName, userLogin, userPassword, email, applicationserver_request=None):
        """
        Add a user account to a sub-space

        @param subSpace: Name of the sub-space
        @type subSpace: string
        @param userFirstName: First name of the user
        @type userFirstName: string
        @param userLastName: Last name of the user
        @type userLastName: string
        @param userLogin: User login to access the new space
        @type userLogin: string
        @param userPassword: User password to access the new space
        @type userPassword: string
        @param email: E-mail address to reach the customer
        @type email: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def listUsers(self, subSpace, applicationserver_request=None):
        """
        List of all user accounts in this sub-space

        @param subSpace: Name of the sub-space
        @type subSpace: string
        @return: dict, {userLogin:{firstName::string,;lastName:string,email:string},...}
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def deleteUser(self, subSpace, userLogin, applicationserver_request=None):
        """
        Delete a user account from the sub-space

        @param subSpace: Name of the sub-space
        @type subSpace: string
        @param userLogin: Login of the user account which you want to delete
        @type userLogin: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def updateUser(self, subSpace, userLogin, userFirstName, userLastName, userPassword, email, applicationserver_request=None):
        """
        Update the information of a user account. If the value of a parameter is empty, the original value is taken

        @param subSpace: Name of the sub-space
        @type subSpace: string
        @param userLogin: User login to access the new space
        @type userLogin: string
        @param userFirstName: First name of the user
        @type userFirstName: string
        @param userLastName: Last name of the user
        @type userLastName: string
        @param userPassword: User password to access the new space
        @type userPassword: string
        @param email: E-mail address to reach the customer
        @type email: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def getCreditInfo(self, subSpace, applicationserver_request=None):
        """
        Get the credit information: total, used and available credits in the subspace

        @param subSpace: Name of the sub-space
        @type subSpace: string
        @return: dict(dict),{total:  {processingCredits: integer, storageCredits: integer, networkCredits:
                 integer},used: {processingCredits: integer, storageCredits: integer, networkingCredits:
                 integer},available: {processingCredits: integer, storageCredits: integer, networkingCredits: integer}}
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def addPublicIpRange(self, subSpace, publicIpRange, applicationserver_request=None):
        """
        Add a public IP range to a Space, required to create VPDCs with public IP addresses

        @param subSpace: Name of the sub-space
        @type subSpace: string
        @param publicIpRange: Name of the public IP range
        @type publicIpRange: string
        @return: True or Error
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def removePublicIpRange(self, subSpace, publicIpRange, applicationserver_request=None):
        """
        Remove a public IP range from a Space. This function fails if the public IP range is still in use in a VPDC

        @param subSpace: Name of the sub-space
        @type subSpace: string
        @param publicIpRange: Name of the public IP range
        @type publicIpRange: string
        @return: True or Error
        """
        pass #TODO


class Jobs(CloudApiBase):

    @q.manage.applicationserver.expose_authenticated
    def list(self, applicationserver_request=None):
        """
        List all the jobs linked to this subspace, return the id and a short description

        @return: array(dict)  , [{ID: integer, status:string,qactionName: string,rootobjectName: string,starttime:
                 string, endtime:string}]
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def getDetailedInfo(self, id, applicationserver_request=None):
        """
        Get detailed info of a specific job

        @param id: identifier for the job
        @type id: integer
        @return: dict
        """
        pass #TODO