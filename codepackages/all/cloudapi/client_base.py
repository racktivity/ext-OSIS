class CloudApiClient:
    def __init__(self, proxy):
        self._proxy = proxy


class Machine(CloudApiClient):
    def createByIP(self, vpdc, name, templateName, description, ipAddresses, capacityProperties, properties):
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
        return self._proxy.cloud_api_machine.createByIP(vpdc, name, templateName, description, ipAddresses, capacityProperties, properties)

    def createByNetwork(self, vpdc, name, templateName, description, publicIPRange, privateNetworks, capacityProperties, properties):
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
        return self._proxy.cloud_api_machine.createByNetwork(vpdc, name, templateName, description, publicIPRange, privateNetworks, capacityProperties, properties)

    def ipAddressAdd(self, vpdc, machine, ipAddress):
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
        return self._proxy.cloud_api_machine.ipAddressAdd(vpdc, machine, ipAddress)

    def ipAddressDelete(self, vpdc, machine, ipAddress):
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
        return self._proxy.cloud_api_machine.ipAddressDelete(vpdc, machine, ipAddress)

    def delete(self, vpdc, machine):
        """
        Remove a machine from a VPDC, but keep the machine in the model.

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine
        @type machine: string
        @return: True or Error
        """
        return self._proxy.cloud_api_machine.delete(vpdc, machine)

    def rename(self, vpdc, oldName, newName):
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
        return self._proxy.cloud_api_machine.rename(vpdc, oldName, newName)

    def setDescription(self, vpdc, machine, description):
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
        return self._proxy.cloud_api_machine.setDescription(vpdc, machine, description)

    def list(self, vpdc):
        """
        list machines in a VPDC

        @param vpdc: Name of VPDC
        @type vpdc: string
        @return: [], list of machine names
        """
        return self._proxy.cloud_api_machine.list(vpdc)

    def start(self, vpdc, machine):
        """
        Start a machine (if machine is hibernated use machine.resume())

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine
        @type machine: string
        @return: True or Error
        """
        return self._proxy.cloud_api_machine.start(vpdc, machine)

    def stop(self, vpdc, machine):
        """
        Shut down a machine

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine
        @type machine: string
        @return: True or Error
        """
        return self._proxy.cloud_api_machine.stop(vpdc, machine)

    def reboot(self, vpdc, machine):
        """
        Reboot a machine

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine
        @type machine: string
        @return: True or Error
        """
        return self._proxy.cloud_api_machine.reboot(vpdc, machine)

    def backup(self, vpdc, machine):
        """
        Create a backup of a machine

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine
        @type machine: string
        @return: True or Error
        """
        return self._proxy.cloud_api_machine.backup(vpdc, machine)

    def listBackups(self, vpdc, machine):
        """
        List with all the backups of a machine

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine
        @type machine: string
        @return: [], list with the names of the backups of the machine
        """
        return self._proxy.cloud_api_machine.listBackups(vpdc, machine)

    def restoreBackup(self, vpdc, machine, backup):
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
        return self._proxy.cloud_api_machine.restoreBackup(vpdc, machine, backup)

    def exportBackup(self, vpdc, machine, backup, target, targetLogin, targetPassword):
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
        return self._proxy.cloud_api_machine.exportBackup(vpdc, machine, backup, target, targetLogin, targetPassword)

    def listCapacityProperties(self, vpdc, machine):
        """
        List all Capacity Properties and their corresponding values on a machine

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine
        @type machine: string
        @return: dict, "capacityProperty: string"
        """
        return self._proxy.cloud_api_machine.listCapacityProperties(vpdc, machine)

    def listProperties(self, vpdc, machine):
        """
        List of all properties of a machine and their corresponding values

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine
        @type machine: string
        @return: dict, "property: string"
        """
        return self._proxy.cloud_api_machine.listProperties(vpdc, machine)

    def setCapacityProperty(self, vpdc, machine, capacityproperty, value):
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
        return self._proxy.cloud_api_machine.setCapacityProperty(vpdc, machine, capacityproperty, value)

    def setProperty(self, vpdc, machine, property, value):
        """
        Set a value for a property on a machine

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine
        @type machine: string
        @return: True or Error
        """
        return self._proxy.cloud_api_machine.setProperty(vpdc, machine, property, value)

    def getMachineDetails(self, vpdc, machine):
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
        return self._proxy.cloud_api_machine.getMachineDetails(vpdc, machine)

    def executeQshellScript(self, vpdc, machine, qshellScriptContent):
        """
        Execute a Q-Shell script on a machine. This function requires a Q-Agent on the machine

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine
        @type machine: string
        @return: dict, {"jobGuid: string,status:string}
        """
        return self._proxy.cloud_api_machine.executeQshellScript(vpdc, machine, qshellScriptContent)

    def copyFromTemplate(self, sourcevpdc, targetvpdc, machine, nameOfCopy):
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
        return self._proxy.cloud_api_machine.copyFromTemplate(sourcevpdc, targetvpdc, machine, nameOfCopy)


class Publiciprange(CloudApiClient):
    def list(self):
        """
        List of all public IP ranges

        @return: dict, {publicIPRangeName:"StartIPAddress-StopIPAddress",...}
        """
        return self._proxy.cloud_api_publiciprange.list()

    def listInVpdc(self, vpdc):
        """
        List of all public IP ranges in a VPDC

        @param vpdc: Name of VPDC
        @type vpdc: string
        @return: dict, {publicIPRangeName:"StartIPAddress-StopIPAddress",...}
        """
        return self._proxy.cloud_api_publiciprange.listInVpdc(vpdc)

    def listWithFreeIPAddresses(self):
        """
        List of all public IP ranges which have one or more free IP addresses

        @return: dict, The keys are the names of the public IP ranges, the values are lists of free IP Addresses.
                 Public IP ranges without free addresses are not included. (So an empty list will never appear as
                 value.)
                 Example: {publicipRangeName, ["1.2.3.4", "1.2.3.6"],...}
        """
        return self._proxy.cloud_api_publiciprange.listWithFreeIPAddresses()

    def listFreeIPFromIPRange(self, name):
        """
        List of free IP addresses in a public IP range. If the name is empty, you get the free IP addresses of all
        public IP ranges

        @param name: Name of a public IP range. The name is unique within space
        @type name: string
        @return: [], list of free IP addresses
        """
        return self._proxy.cloud_api_publiciprange.listFreeIPFromIPRange(name)

    def rename(self, oldName, newName):
        """
        Rename a public IP range, the original name is given by the cloud provider, the cloud user can change it.

        @param oldName: Name of the public IP range, given by the cloud provider
        @type oldName: string
        @param newName: New name of the public IP range
        @type newName: string
        @return: True or Error
        """
        return self._proxy.cloud_api_publiciprange.rename(oldName, newName)

    def getDetails(self, name):
        """
        Get the details of a public IP range

        @param name: Name of a public IP range. The name is unique within space
        @type name: string
        @return: dict, {name: string, customer: string, network: string, netmask: string,startiprange:
                 string,stopiprange: string,gateway: string, domainnameservers: string}
        """
        return self._proxy.cloud_api_publiciprange.getDetails(name)

    def split(self, name, newIpRangeName, nrOfIps):
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
        return self._proxy.cloud_api_publiciprange.split(name, newIpRangeName, nrOfIps)

    def delete(self, name):
        """
        Delete a public IP range

        @param name: Name of a public IP range. The name is unique within space
        @type name: string
        @return: True or Error
        """
        return self._proxy.cloud_api_publiciprange.delete(name)


class Privatenetwork(CloudApiClient):
    def list(self):
        """
        List of all private networks

        @return: array(dict)  [{privateNetworkName:name, network:aipaddr, subnet:mask}]
        """
        return self._proxy.cloud_api_privatenetwork.list()

    def listInVpdc(self, vpdc):
        """
        List of all private networks in a VPDC

        @param vpdc: Name of VPDC
        @type vpdc: string
        @return: array(dict)  [{privateNetworkName:name, network:aipaddr, subnet:mask}]
        """
        return self._proxy.cloud_api_privatenetwork.listInVpdc(vpdc)

    def rename(self, oldName, newName):
        """
        Rename a private network, the original name is automatically created when a private network is needed

        @param oldName: Name of the public IP range, given by the cloud provider
        @type oldName: string
        @param newName: New name of the public IP range
        @type newName: string
        @return: True or Error
        """
        return self._proxy.cloud_api_privatenetwork.rename(oldName, newName)

    def listFreeIP(self, name):
        """
        List of free IP addresses in a private network. A name of the private network must be provided with this
        function

        @param name: Name of a public IP range. The name is unique within space
        @type name: string
        @return: [], list of free IP addresses
        """
        return self._proxy.cloud_api_privatenetwork.listFreeIP(name)

    def create(self, name):
        """
        Create a new private network. The cloud software will make sure a new VLAN (or comparable technology) is created
        with a unique name in the cloud domain.

        @param name: Name of a public IP range. The name is unique within space
        @type name: string
        @return: True or Error
        """
        return self._proxy.cloud_api_privatenetwork.create(name)

    def getDetails(self, name):
        """
        Get the details of a private network

        @param name: Name of a public IP range. The name is unique within space
        @type name: string
        @return: {}, {name: string, customer: string, network: string, netmask: string,gateway: string,
                 domainnameservers: string}
        """
        return self._proxy.cloud_api_privatenetwork.getDetails(name)

    def delete(self, name):
        """
        Delete a private network if no machine is using it. An error is thrown if a machine uses the private network

        @param name: Name of a public IP range. The name is unique within space
        @type name: string
        @return: True or Error
        """
        return self._proxy.cloud_api_privatenetwork.delete(name)


class Machinetemplate(CloudApiClient):
    def list(self):
        """
        List of all available machine templates

        @return: tuple of machine template names
        """
        return self._proxy.cloud_api_machinetemplate.list()

    def getDetails(self, machineTemplate):
        """
        Get the details of a machine template

        @param machineTemplate: Name of the template
        @type machineTemplate: string
        @return: dict, {name:string, description: string, Type: string, OS: string, capacityProperties:
                 {propertyName(string): value(string), ...}, properties: {propertyName(string): value(string), ...},
                 Ports:{portName(string): {Type: string,capacityProperties: {propertyName(string): value(string), ...}},
                 ...}}
        """
        return self._proxy.cloud_api_machinetemplate.getDetails(machineTemplate)


class Portal(CloudApiClient):
    def getVersion(self):
        """
        This function is only to check the version of the CloudAPI

        @return: string, Version of the CloudAPI
        """
        return self._proxy.cloud_api_portal.getVersion()


class Vpdc(CloudApiClient):
    def create(self, vpdc):
        """
        Create a new VPDC, based on a VPDC-template

        @param vpdc: Name of VPDC
        @type vpdc: string
        @return: string, name of the VPDC
        """
        return self._proxy.cloud_api_vpdc.create(vpdc)

    def delete(self, vpdc):
        """
        Delete a VPDC

        @param vpdc: Name of VPDC
        @type vpdc: string
        @return: True or Error
        """
        return self._proxy.cloud_api_vpdc.delete(vpdc)

    def deploy(self, vpdc):
        """
        Deploy a VPDC

        @param vpdc: Name of VPDC
        @type vpdc: string
        @return: True or Error
        """
        return self._proxy.cloud_api_vpdc.deploy(vpdc)

    def list(self):
        """
        Get a list of all VPDCs

        @return: tuple of VPDC names
        """
        return self._proxy.cloud_api_vpdc.list()

    def start(self, vpdc):
        """
        Start all machines in a VPDC

        @param vpdc: Name of VPDC
        @type vpdc: string
        @return: True or Error
        """
        return self._proxy.cloud_api_vpdc.start(vpdc)

    def stop(self, vpdc):
        """
        Stop all machines in a VPDC

        @param vpdc: Name of VPDC
        @type vpdc: string
        @return: True or Error
        """
        return self._proxy.cloud_api_vpdc.stop(vpdc)

    def getDeployStatus(self, vpdc):
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
        return self._proxy.cloud_api_vpdc.getDeployStatus(vpdc)


class Subspace(CloudApiClient):
    def create(self, subSpace, processingCredits, storageCredits, networkingCredits, userFirstName, userLastName, userLogin, userPassword, email):
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
        return self._proxy.cloud_api_subspace.create(subSpace, processingCredits, storageCredits, networkingCredits, userFirstName, userLastName, userLogin, userPassword, email)

    def delete(self, subSpace):
        """
        Delete a sub-space

        @param subSpace: Name of the sub-space
        @type subSpace: string
        @return: True or Error
        """
        return self._proxy.cloud_api_subspace.delete(subSpace)

    def listSubSpaces(self):
        """
        List all sub-spaces

        @return: tuple of sub-space names
        """
        return self._proxy.cloud_api_subspace.listSubSpaces()

    def addUser(self, subSpace, userFirstName, userLastName, userLogin, userPassword, email):
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
        return self._proxy.cloud_api_subspace.addUser(subSpace, userFirstName, userLastName, userLogin, userPassword, email)

    def listUsers(self, subSpace):
        """
        List of all user accounts in this sub-space

        @param subSpace: Name of the sub-space
        @type subSpace: string
        @return: dict, {userLogin:{firstName::string,;lastName:string,email:string},...}
        """
        return self._proxy.cloud_api_subspace.listUsers(subSpace)

    def deleteUser(self, subSpace, userLogin):
        """
        Delete a user account from the sub-space

        @param subSpace: Name of the sub-space
        @type subSpace: string
        @param userLogin: Login of the user account which you want to delete
        @type userLogin: string
        @return: True or Error
        """
        return self._proxy.cloud_api_subspace.deleteUser(subSpace, userLogin)

    def updateUser(self, subSpace, userLogin, userFirstName, userLastName, userPassword, email):
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
        return self._proxy.cloud_api_subspace.updateUser(subSpace, userLogin, userFirstName, userLastName, userPassword, email)

    def getCreditInfo(self, subSpace):
        """
        Get the credit information: total, used and available credits in the subspace

        @param subSpace: Name of the sub-space
        @type subSpace: string
        @return: dict(dict),{total:  {processingCredits: integer, storageCredits: integer, networkCredits:
                 integer},used: {processingCredits: integer, storageCredits: integer, networkingCredits:
                 integer},available: {processingCredits: integer, storageCredits: integer, networkingCredits: integer}}
        """
        return self._proxy.cloud_api_subspace.getCreditInfo(subSpace)

    def addPublicIpRange(self, subSpace, publicIpRange):
        """
        Add a public IP range to a Space, required to create VPDCs with public IP addresses

        @param subSpace: Name of the sub-space
        @type subSpace: string
        @param publicIpRange: Name of the public IP range
        @type publicIpRange: string
        @return: True or Error
        """
        return self._proxy.cloud_api_subspace.addPublicIpRange(subSpace, publicIpRange)

    def removePublicIpRange(self, subSpace, publicIpRange):
        """
        Remove a public IP range from a Space. This function fails if the public IP range is still in use in a VPDC

        @param subSpace: Name of the sub-space
        @type subSpace: string
        @param publicIpRange: Name of the public IP range
        @type publicIpRange: string
        @return: True or Error
        """
        return self._proxy.cloud_api_subspace.removePublicIpRange(subSpace, publicIpRange)


class Jobs(CloudApiClient):
    def list(self):
        """
        List all the jobs linked to this subspace, return the id and a short description

        @return: array(dict)  , [{ID: integer, status:string,qactionName: string,rootobjectName: string,starttime:
                 string, endtime:string}]
        """
        return self._proxy.cloud_api_jobs.list()

    def getDetailedInfo(self, id):
        """
        Get detailed info of a specific job

        @param id: identifier for the job
        @type id: integer
        @return: dict
        """
        return self._proxy.cloud_api_jobs.getDetailedInfo(id)