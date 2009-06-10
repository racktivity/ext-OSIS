class Disk(CloudApiBase):

    @q.manage.applicationserver.expose_authenticated
    def listDisks(self, vpdc, machine, applicationserver_request=None):
        """
        List all disks for the machine specified

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine. The name is a freely chosen name, which has to be unique in SPACE
        @type machine: string
        @return: dict, {"disk": string, "properties": {"name": string, "type": string, "iscsitarget": boolean}} #Return
                 a dict where disk is the guid of the disk and properties is a dict of most relevant disk properties
        """
        """
        Implementation:
        ********************
        Retrieve disks from model using drp client
        """

        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def listSnapshots(self, vpdc, machine, disk, applicationserver_request=None):
        """
        List all snapshots for the machine and disk specified

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine. The name is a freely chosen name, which has to be unique in SPACE
        @type machine: string
        @param disk: GUID of the disk
        @type disk: string
        @return: dict, {"snapshot": string, "properties": {"name": string, "creationdate": string}} #Return a dict where
                 snapshot is the guid of the snapshot and properties is a dict of most relevant snapshot properties
        """
        """
        Implementation:
        ********************
        Retrieve snapshots from model using drp client
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def exposeISCSITarget(self, vpdc, machine, disk, snapshot, applicationserver_request=None):
        """
        Create a clone of the snapshot specified and expose it as an ISCSI target

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine. The name is a freely chosen name, which has to be unique in SPACE
        @type machine: string
        @param disk: GUID of the disk
        @type disk: string
        @param snapshot: GUID of the snapshot
        @type snapshot: string
        @return: string #ISCSI IQN of the newly exposed target
        """
        """
        Implementation:
        ********************
        * Resolve Q-Store hosting the ZVOL by using the model
        * Execute PyMonkey commands over SSH -> Is also part of PyMonkey framework
        * Use ZFS + iscsitadm PyMonkey extensions on remote systems to create clone + ISCSI target
        * Clone the snapshot
        * Expose as new ISCSI target
        * Put new target in model as disk using drp client
        """
        pass #TODO

    @q.manage.applicationserver.expose_authenticated
    def removeISCSITarget(self, vpdc, machine, disk, applicationserver_request=None):
        """
        Delete the ISCSI target for the disk

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine. The name is a freely chosen name, which has to be unique in SPACE
        @type machine: string
        @param disk: GUID of the disk
        @type disk: string
        @return: True or Error
        """
        """
        Implementation:
        ********************
        * Resolve Q-Store hosting the ZVOL by using the model
        * Execute PyMonkey commands over SSH -> Is also part of PyMonkey framework
        * Use ZFS + iscsitadm PyMonkey extensions on remote systems to remove ISCSI target
        * Remove clone
        * Remove disk from model using drp client
        """
        pass #TODO
