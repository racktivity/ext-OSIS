
# TODO cleanup + doc


namespace = "core.disk"

## @doc  properties of a disk
class disk(RootObject):
    
    ## @doc  name of the device to which the disk belongs
    ## @type type_path
    devicename
    
    ## @doc  size of the disk, unit in GB
    ## @type int
    size
    
    ## @doc  path to the image, which is installed on the disk
    ## @type type_url
    imagepath
    
    ## @doc  type of the disk
    ## @db   notnull indexed
    ## @type disktype
    type
    
    ## TODO: add doc
    ## @type int
    order
    
    ## @doc  guid of the disk used to create this disk
    ## @bizz ref = disk
    ## @db   indexed
    ## @type guid
    connecteddiskguid
    
    ## @doc  iqn (iSCSI Qualified Name) of the disk
    ## @type type_iqn
    iqn
    
    ## @doc  status of the disk
    ## @db   indexed notnull
    ## @type diskstatustype
    status
    
    ## @doc  size of a disk sector
    ## @type int
    sectorsize
    
    ## @doc  checksum of the image to verify the validity of the image
    ## @type string(32)
    imagechecksum
    
    ## @doc  include disk in backup
    ## @type boolean
    backup = True
    
    ## @doc  role of the disk (boot, data, swap)
    ## @db   notnull indexed
    ## @type diskroletype
    role
    
    ## @doc  list of partitions on the disk
    ## @type array(partition)
    partitions
    


#TODO capacityunitconsumed ?

class capacityunitprovided(DRPObject):
    
    ## @doc  amount of storage units consumed by the disk
    ## @type int
    amount
    
    ## @doc  type of capacity unit
    ## @db   notnull indexed
    ## @type capacityunittype
    type
    

class filesystem(DRPObject):
    
    ## @doc  name of the device on which the file system is located
    ## @type type_path
    devicename
    
    ## @doc  mountpoint of the file system
    ## @type type_path
    mountpoint
    
    ## @doc  list of snapshots taken from the file system
    ## @type array(filesystemsnapshot)
    snapshots
    

class filesystemsnapshot(DRPObject):
    
    ## @doc  name of the device on which the file system is located
    ## @type type_path
    devicename
    
    ## @doc  mountpoint of the file system from which the snapshot is taken
    ## @type type_path
    mountpoint
    

class filesystempartitionsnapshot(DRPObject):
    
    ## @doc  name of the device on which the file system is located
    ## @type type_path
    devicename
    
    ## @doc  mountpoint of the file system from which the snapshot is taken
    ## @type type_path
    mountpoint

 
class partition(DRPObject):
    
    ## @doc  list of file systems, created on the partition
    ## @db   notnull indexed
    ## @type array(filesystem)
    filesystems

    ## @doc  size of the partition, expressed in GB
    ## @type int
    size
    
    ## @doc  partition id on the disk
    ## @db   notnull
    ## @type int
    order
    
    ## @doc  path to the image which is installed on the partition
    ## @type type_path
    imagepath
    
    ## @doc  checksum to verify the validity of the partition
    ## @type string(32)
    imagechecksum

    ## @doc  indicate whether to include the partition for a backup or not
    ## @type boolean    
    backup = True

    #TODO semantics    
    ## @type boolean
    boot = True
    
    ## @doc  size of the image that will be installed on the partition
    ## @type int
    imagesize
    
    ## @doc  status of the partition
    ## @db   notnull indexed
    ## @type partitionstatustype
    status
    
    ## @doc  number which indicates the first sector of the partition
    ## @type int
    sectorstart
    
    ## @doc  number which indicates the last sector of the partition
    ## @type int
    sectorend
    
    #TODO: what is this, verify with order
    ## @type int
    number
    
    ## @doc  list of snapshots, taken from the partition
    ## @type array(partitionsnapshot)
    snapshots
   


 
class partitionsnapshot(DRPObject):
    
    ## @doc  list of file systems, created on the partition
    ## @db   notnull indexed
    ## @type array(filesystempartitionsnapshot)
    filesystems

    ## @doc  size of the snapshot
    ## @type int
    size
    
    #TODO: what is this
    ## @db   notnull
    ## @type int
    order
    
    ## @doc  path to the image, installed on the partition from which a snapshot is taken
    ## @type type_path
    imagepath
    
    ## @doc  checksum to verify the validity of the snapshot
    ## @type string(32)
    imagechecksum

    #TODO: what is this
    ## @type boolean    
    backup = True

    #TODO semantics    
    ## @type boolean
    boot = True
    
    #TODO: what is this
    ## @type int
    imagesize
    
    #TODO: what is this
    ## @db   notnull indexed
    ## @type partitionstatustype
    status
    
    #TODO: what is this
    ## @type int
    sectorstart
    
    #TODO: what is this
    ## @type int
    sectorend
    
    #TODO: what is this
    ## @type int
    number
    
    
    
    
class partitionstatustype(QType):
    ##+ name = "CONFIGURED"
    ##+ name = "CREATED"
    
    
class filesystemtype(QType):
    ##+ name = "LINUX-SWAP"
    ##+ name = "EXT3"
    ##+ name = "REISERFS"
    ##+ name = "XFS"
    ##+ name = "NTFS"
    ##+ name = "EXT2"
    ##+ name = "FAT32"
    
    
class disktype(QType):
    ##+ name = "VOLUME"
    ##+ name = "FILE"
    ##+ name = "SWAP"
    ##+ name = "RAWDEVICE"
    ##+ name = "QSANVOLUME"
    ##+ name = "QSANTARGET"
    ##+ name = "QSANCONNECTOR"
    ##+ name = "QSTOREVOLUME"
    ##+ name = "QSTORETARGET"
    ##+ name = "QSTORECONNECTOR"
    ##+ name = "VMDKBACKUP"
    ##+ name = "QSTOREBACKUP"
    ##+ name = "VMDK"
    ##+ name = "ISCSITARGET"


class diskstatustype(QType):
    ##+ name = "CONFIGURED"
    ##+ name = "CREATED"


class diskroletype(QType):
    ##+ name = "TEMP"
    ##+ name = "BOOT"
    ##+ name = "DATA"
    

#TODO should move to vpdc model
class capacityunittype(QType):
    
    ##+ name = "SUA"         # storage unit A
    ##+ name = "SUB"         # storage unit B
    ##+ name = "SUC"         # storage unit C
    
    ##+ name = "LV"          # Linux vmachines
    ##+ name = "WV"          # Windows vmachines
    
    ##+ name = "NUIPPORTS"   # network unit public ip address
    ##+ name = "NUM"         # network unit bandwidth in Mbit/s
    ##+ name = "NBU"         # network bandwidth units
    
    ##+ name = "lan"        # lan (?)
    
    ##+ name = "PU"          # processing unit
    
