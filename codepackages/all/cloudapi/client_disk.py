class CloudApiClient:
    def __init__(self, proxy):
        self._proxy = proxy


class Disk(CloudApiClient):
    def listDisks(self, vpdc, machine):
        """
        List all disks for the machine specified

        @param vpdc: Name of VPDC
        @type vpdc: string
        @param machine: Name of the machine. The name is a freely chosen name, which has to be unique in SPACE
        @type machine: string
        @return: dict, {"disk": string, "properties": {"name": string, "type": string, "iscsitarget": boolean}} #Return
                 a dict where disk is the guid of the disk and properties is a dict of most relevant disk properties
        """
        return self._proxy.cloud_api_disk.listDisks(vpdc, machine)

    def listSnapshots(self, vpdc, machine, disk):
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
        return self._proxy.cloud_api_disk.listSnapshots(vpdc, machine, disk)

    def exposeISCSITarget(self, vpdc, machine, disk, snapshot):
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
        return self._proxy.cloud_api_disk.exposeISCSITarget(vpdc, machine, disk, snapshot)

    def removeISCSITarget(self, vpdc, machine, disk):
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
        return self._proxy.cloud_api_disk.removeISCSITarget(vpdc, machine, disk)