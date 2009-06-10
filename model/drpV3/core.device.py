
namespace = "core.device"


## @doc  physical device that you put in a rack e.g. physical computer, switch, UPS
class device(RootObject):

    ## @doc  device type
    ## @db   notnull indexed
    ## @type devicetype
    type

    ## @doc  guid of the rack to which the device belongs - can be None e.g. for devices in stock or in repair
    ## @db   indexed
    ## @bizz ref = core.rack/rack
    ## @type guid
    rackguid
 
    ## @doc  guid of the datacenter to which the device belongs 
    ## @db   notnull indexed
    ## @bizz ref = core.datacenter/datacenter
    ## @type guid
    datacenterguid

    ## @doc  size of the device, measured in u e.g. 1u high
    ## @type int
    racku = 1

    ## @doc  physical position of the device in a rack (y coordinate) measured in u slots
    ##       The position starts at bottom of rack, starting with 1
    ## @type int
    racky = 0

    ## @doc  physical position of the device in the rack (z coordinate, 0 = front, 1 = back)
    ## @type int
    rackz = 0

    ## @doc  model number of the device
    ## @type string(60)
    modelnr

    ## @doc  serial number of the device
    ## @type string(60)
    serialnr

    ## @doc  firmware identifier of the device
    ## @type string(60)
    firmware

    ## @doc  remarks on the device
    ## @type type_description
    remark

    ## @doc  last time device was inspected
    ## @type type_date
    lastcheck

    ## @doc  device status
    ## @db   indexed notnull
    ## @type devicestatustype
    status

    # TODO: what are the semantics
    ## @doc  parent device
    ## @bizz ref = device
    ## @db   indexed
    ## @type guid
    parentdeviceguid

    ## @doc  resource pool to which the device belongs 
    ## @db   notnull indexed
    ## @bizz ref = core.resourcepool/resourcepool
    ## @type guid
    resourcepoolguid
   
    ## @doc  list of components which are part of the device 
    ## @type array(component)
    components

    # TODO does not belong here -- not every device has disks? e.g. switch / airco
    ## @doc  disks which are part of device 
    ## @type array(disk)
    disks

    # TODO does this belong here? see disks
    ## @doc  nicports which are part of device    
    ## @type array(nicport)
    nicports
    
    ## @doc  date and time of last check on the device with reality
    ## @type type_date
    lastrealitycheck
     
    ## @doc  list of capacity units, consumed by the device (e.g. power)
    ## @type array(capacityunit)
    capacityunitsconsumed
    
    ## @doc  list of capacity units, provided by the device
    ## @type array(capacityunit)
    capacityunitsprovided    
    
## @doc  device status
class devicestatustype(QType):
    ##+ name = "BROKEN"
    ##+ name = "ACTIVE"
    ##+ name = "SLEEPING"
    ##+ name = "INREPAIR"
    ##+ name = "INSTOCK"



## @doc  physical disk 
class disk(DRPObject):
       
    ## @doc  disk size in GB e.g. 160
    ## @type int
    size
    
    ## @doc  disk rotations per minute e.g. 7200
    ## @type int
    rpm

    ## @doc  disk interface type        
    ## @db   notnull indexed
    ## @type diskinterfacetype
    type

    ## @doc  disk status        
    ## @db   indexed notnull
    ## @type diskstatustype
    status

    ## TODO: discuss do we need this relation?
    ## @doc  component information about the disk
    ## @bizz ref = component
    ## @db   indexed
    ## @type guid
    componentguid



## @doc  physical disk interface type
class diskinterfacetype(QType):
    ##+ name = "SATA"
    ##+ name = "SCSI"
    ##+ name = "FC"



## @doc  disk status
class diskstatustype(QType):
    ##+ name = "BROKEN"
    ##+ name = "ACTIVE"
    ##+ name = "SLEEPING"
    ##+ name = "INSTOCK"



## @doc  physical network interface in a device
class nicport(DRPObject):

    ## @doc  hardware type of nicport               
    ## @db   notnull indexed
    ## @type nicporttype
    type

    ## @doc  status of nicport        
    ## @db   indexed notnull
    ## @type nicportstatustype
    status
    
    ## @doc  hardware address like macaddr
    ## @db   indexed 
    ## @type string
    hwaddr

    ## @doc  backplane to which the nicport is connected
    ## @bizz ref = core.domain/backplane
    ## @db   indexed
    ## @type guid
    backplaneguid
   
    ## @doc  cable to which the nicport is connected 
    ## @db   indexed
    ## @type guid
    cableguid

    # TODO do we need this - see above
    ## @doc  component information of nicport
    ## @bizz ref = component
    ## @db   indexed
    ## @type guid
    componentguid

    ## #doc  guid of the group of nicports
    ## @bizz ref = core.machine/nicportgroup
    ## @db   indexed
    ## @type guid
    nicportgroupguid 

## @doc  type of physical network interface    
class nicporttype(QType):
    ##+ name = "ETHERNET_10MB"
    ##+ name = "ETHERNET_100MB"
    ##+ name = "ETHERNET_GB"
    ##+ name = "ETHERNET_10GB"
    ##+ name = "INFINIBAND"
    ##+ name = "FC"        



## @doc  status of physical network interface
class nicportstatustype(QType):
    ##+ name = "BROKEN"
    ##+ name = "ACTIVE"
    ##+ name = "NOTCONNECTED"



## @doc  device account e.g. BIOS account, firmware account
class account(DRPObject):

    ## @doc  device account type
    ## @db   notnull indexed
    ## @type accounttype
    type

    ## @doc  device account login
    ## @type type_login
    login

    ## @doc  device account password
    ## @type type_password
    password



## @doc  a device consists of components
class component(DRPObject):

    ## @doc  component brand
    ## @db   notnull indexed
    ## @type componentbrandtype
    brand

    ## @doc  component type
    ## @db   notnull indexed
    ## @type componenttype
    type

    ## @doc  component model identification
    ## @type string(30)
    modelnr

    ## @doc  component serial number
    ## @type string(30)
    serialnr

    ## @doc  batch number, can be used to identify components belonging to a bad vendor batch
    ## @type string(30)
    batchnr

    ## @doc  firmware version
    ## @type string(30)
    firmware

    ## @doc  label
    ## @type string(30)
    label

    # TODO: relation to port was removed


#TODO: I removed port, portgroup, portgrouptype, portstatustype

#class porttype(QType):
#    ##+ name="ETHERNET", description="Ethernet port"
#    ##+ name="SATA", description="SATA port"
#    ##+ name="ACPOWER", description="ac power port"
#    ##+ name="PARALLEL", description="Parallel port"
#    ##+ name="WIRELESS", description="Wireless network adapter"
#    ##+ name="IR", description="Infrared port"
#    ##+ name="SERIAL", description="Serial port"
#    ##+ name="FIREWIRE", description="Firewire port"
#    ##+ name="USB", description="USB port"

#class portstatustype(QType): 
#    ##+ name="ENABLED",  description="port is enabled"
#    ##+ name="DISABLED", description="port is disabled"


## @doc  component brand/vendor
class componentbrandtype(QType):
    ##+ name="INTEL"
    ##+ name="SEAGATE"
    ##+ name="MAXTOR"
    ##+ name="WESTERN_DIGITAL"
    ##+ name="AMD"
    ##+ name="SUPERMICRO"



## @doc  component type
class componenttype(QType): 
    ##+ name="SWC",  description="Switch portcontainer"
    ##+ name="PWC",  description="Powerswitch portcontainer"
    ##+ name="NIC",  description="Network Adapter"
    ##+ name="USPC", description="UPS portcontainer"
    ##+ name="CPU",  description="CPU"
    ##+ name="MB",   description="Mainboard"
    ##+ name="HDD",  description="Harddrive"
    ##+ name="MEM",  description="Memory"
    

#TODO devicetype POOL used for a pool of disks which are in stock or repair

## @doc  device type
class devicetype(QType):
    ##+ name="AIRCO"
    ##+ name="COMPUTER"
    ##+ name="POWERSWITCH"
    ##+ name="SWITCH"
    ##+ name="UPS"
    ##+ name="POOL", description="device of type POOL can be used to contain a set of disks and components which are in stock or in repair"
    
class accounttype(QType):
    
    ##+ name = "BIOSACCOUNT"

class capacityunit(DRPObject):
    
    ## @doc  amount of capacity units
    ## @type int
    amount
    
    ## @doc  type of capacity unit
    ## @db   notnull indexed
    ## @type capacityunittype
    type    
    
class capacityunittype(QType):
    
    ##+ name = "SUA"         # storage unit Archive
    ##+ name = "SUP"         # storage unit Primary
    
    ##+ name = "LV"          # Linux vmachines
    ##+ name = "WV"          # Windows vmachines
    
    ##+ name = "NUIPPORTS"   # network unit public ip address
    ##+ name = "NUM"         # network unit bandwidth in Mbit/s
    ##+ name = "NBU"         # network bandwidth units in GB/month
    
    ##+ name = "MU"          # memory unit (MB)
    ##+ name = "CU"          # CPU unit (mhz) 
    
 