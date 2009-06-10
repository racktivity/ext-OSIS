
namespace = "core.machine"

## @doc  class which sets the provides the properties of a machine
class machine(RootObject):

    ## @doc  alias of the machine, can be a more meaningful name
    ## @type type_alias
    alias
    
    ## @doc  unique identifier of the machine
    ## @db   unique notnull
    ## @type type_assetid
    assetid

    ## @doc  hostname of the machine
    ## @type type_hostname
    hostname

    ## @doc  number of CPU's in the machine
    ## @type int
    nrcpu

    ## @doc  cumulative CPU frequency in MHz (e.g. 2 quadcore cpus of each 2GHz has a cumulative cpu frequency of 16,384 MHz)
    ## @type int
    cpufrequency

    ## @doc  memory allocated to machine in gigabyte
    ## @type int
    memory

    ## @doc  date and time of last check on the machine
    ##       The
    ## @type type_date
    lastrealitycheck
    
    ## @doc  custom settings and configuration of machine, is XML, to be used freely
    ## @type string
    customsettings

    ## @doc  flag indicating that this machine must be automatically started when rebooting the parent machine 
    ## @type boolean
    boot = False

    ## @doc  guid of the parent device    
    ## @bizz ref = core.device/device
    ## @db   indexed
    ## @type guid
    deviceguid
    
    ## @doc default gateway ip addr
    ## @type type_ipaddress
    defaultgateway    
        
    ## @doc  status of the machine
    ## @db   indexed notnull
    ## @type machinestatustype
    status

    #TODO monitoring policy namespace
    ## @doc  guid of the policy that monitors this machine
    ## @db   indexed
    ## @type guid
    monitoringpolicyguid

    ## @doc  guid of the customer, owning this machine    
    ## @db   notnull indexed
    ## @bizz ref = core.customer/customer
    ## @type guid
    customerguid
    
    ## @doc  type of the machine, is textual description
    ## @db   notnull indexed
    ## @type string(10)
    type
    
    ## @doc  guid of the parent machine that hosts the machine
    ## @bizz ref = core.machine/machine
    ## @db   indexed
    ## @type guid
    parentmachineguid
    
    ## @doc  guid of the domain in which the machine resides
    ## @db   notnull indexed
    ## @bizz ref = core.domain/domain
    ## @type guid
    domainguid

    ## @doc  hypervisor running this machine (only applicable for virtual machines)    
    ## @db   notnull indexed
    ## @type hypervisortype
    hypervisor

    ## @doc  list of file systems on the machine
    ## @type array(filesystem)
    filesystems
    
    ## @doc  list of disks in the machine
    ## @type array(disk)
    disks
    
    ## @doc  list of accounts who can access the machine
    ## @type array(account)
    accounts

    ## @doc  os of machine
    ## @type os
    os
   
    ## @doc  list of NICs on the machine
    ## @type array(nic)
    nics
    
    ## @doc  lan's are part of one or more vdc's
    ## @bizz ref = cloud.vdc/vdc
    ## @db   indexed
    ## @type array(guid)
    vdcguids    
    
    ## @doc  vmachine hosts 1 or more applications
    ## @bizz ref = core.application/application
    ## @type array(guid)
    applicationguids

    ## @doc  list of capacity units, consumed by the machine
    ## @type array(capacityunit)
    capacityunitsconsumed
    
    ## @doc  list of capacity units, provided by the machine
    ## @type array(capacityunit)
    capacityunitsprovided

class capacityunitconsumed(DRPObject):
    
    ## @doc  amount of capacity units, consumed by the machine
    ## @type int
    amount
    
    ## @doc  type of capacity unit
    ## @db   notnull indexed
    ## @type capacityunittype
    type

class capacityunitprovided(DRPObject):
    
    ## @doc  amount of capacity units, provided by the machine
    ## @type int
    amount
    
    ## @doc  type of capacity unit
    ## @db   notnull indexed
    ## @type capacityunittype
    type
        
class nic(DRPObject):
    
    ## @doc  flag indicating if the NIC is disabled
    ##       Default the value is False
    ## @type boolean
    disabled=False
    
    ## @doc  guid of the Q-LAN to which the NIC belongs
    ## @db   notnull indexed
    ## @bizz ref = core.lan/lan
    ## @type guid
    languid

    ## @doc  NIC order to identify how the NICs come up e.g. 0 for eth0, 1 for eth1
    ## @db   notnull
    ## @type int
    order
    
    ## @doc  type of the NIC, listed in the enumerator nictype
    ## @db   notnull indexed
    ## @type nictype
    type
    
    ## @doc  list of IP addresses on the NIC
    ## @type array(ip)
    ips
    
    ## @doc  MAC address of the NIC
    ## @type string
    hwaddr

    ## @doc  guid of the portgroup to which the NIC belongs
    ## @db   indexed
    ## @bizz ref = core.machine/nicportgroup
    ## @type guid
    portgroupguid
    
    
class ipaddress(DRPObject):
    
    ## @doc  IP address of the IP
    ## @type type_ipaddress
    address
    
    ## @doc  netmask of the IP object
    ## @type type_netmaskaddress
    netmask
    
    ## @doc  subnet to which the IP object belongs
    ## @type type_ipaddress
    subnet
    
    ## @doc  flag indicating if the IP is blocked
    ## @type boolean
    block = False

    ## @doc  type of the IP object, IPv4 or IPv6
    ## @db   notnull indexed
    ## @type iptype
    type
    
    ## @doc  ip addresses linked to this service only, null if not specific to this service, link to guid of ip address as used in machine
    ## @type array(portforwardingservice)
    portforwardingservices    
        
    
## #describes a portforwarding to this ipaddress
class portforwardingservice(DRPObject):
    
    ## @doc  ip address which is used to forward to this ip address
    ## @bizz ref = cloud.machine/ipaddress
    ## @db   indexed
    ## @type guid)   
    hostipaddress
    
    ## @doc  TCP or UDP port number on source ip (the alias which does the forwarding)
    ## @type int
    portnrsource

    ## @doc  TCP or UDP port number on dest ip (on this machine ip)
    ## @type int
    portnrdestination
    
    ## @doc  udp or tcp service
    ## @db   notnull indexed
    ## @type ipprotocoltype
    ipprotocoltype


class ipprotocoltype(QType):
    ##+ name = "UDP"
    ##+ name = "TCP"

class account(DRPObject):
    
    ## @doc  type of the machine account, listed in the enumerator accounttype
    ## @db   notnull indexed
    ## @type accounttype
    type
    
    ## @doc  login of the account to access the machine
    ## @db   notnull
    ## @type type_login
    login
    
    ## @doc  password of the account to access the machine
    ## @type type_password
    password
    

    
#class iptransporttype(QType):
#    ##+ name="UDP"
#    ##+ name="TCP"

class iptype(QType):
    ##+ name="IPV4"

    
class nictype(QType):
    ##+ name = "ETHERNET_10MB"
    ##+ name = "ETHERNET_100MB"
    ##+ name = "ETHERNET_GB"
    ##+ name = "INFINIBAND"
    ##+ name = "VLAN"
  
    
class hypervisortype(QType):
    ##+ name = "KVM"
    ##+ name = "VIRTUALBOX"
    ##+ name = "VMWARE_GSX"
    ##+ name = "VMWARE_ESX"
    ##+ name = "XEN"
    

class machinestatustype(QType):
    ##+ name = "CONFIGURED"
    ##+ name = "IMAGE_ONLY"
    ##+ name = "HALTED"
    ##+ name = "RUNNING"
    ##+ name = "PAUSED"    
    
class accounttype(QType):
    
    ##+ name = "SYSTEMACCOUNT"
    ##+ name = "PUBLICACCOUNT"

## @doc  operating system
class os(RootObject):

    ## @doc  os brand
    ## @db   notnull indexed
    ## @type ostype
    type

    ## @doc  filename of icon representing os in various user interfaces
    ## @type type_name
    iconname
    
    ## @doc  version of the operating system
    ## @type type_description
    version

    ## @doc  patch level of operating system    
    ## @type type_description
    patchlevel

    ## @doc  description of the operating system
    ## @type string(50)
    description
    

## @doc  os type
class ostype(QType):
    ##+ name="WINDOWS"
    ##+ name="SOLARIS"
    ##+ name="OPENSOLARIS"
    ##+ name="LINUX"


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
    