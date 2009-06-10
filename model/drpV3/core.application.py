# Namespace
namespace = "core.application"

## @doc Software application running on a machine, offering services to other applications and networkzones
class application(RootObject):

    ## @doc  status of the application
    ## @db   notnull indexed
    ## @type statustype
    status
   
    ## @doc  is template, when template used as example for an application
    ## @db   notnull indexed
    ## @type bool
    template
    
    
    ## @doc  application name, is free text defined in template e.g. kvm, virtualboxhypervisor, xenhypervisor, sshserver, backupserver, ...
    ## @db   notnull indexed
    ## @type string
    name  

    ## @doc  additional remarks on application
    ## @type type_description
    description       
    
    ## @doc  tells from which machine template this machine object originates (can be null if no template used)
    ## @db   indexed
    ## @type guid
    applicationtemplateguid  
    
    
    ## @doc  guid of the machine on which the application is installed / running
    ## @db   notnull indexed
    ## @bizz ref = core.machine/machine
    ## @type guid
    machineguid   


    ## @doc  custom settings and configuration of application, is XML
    ## @type string
    customsettings
    
    ## @doc  list of services offered by this application to another object
    ##       e.g. KVM to a virtual machine
    ##       e.g. service to a customer
    ## @type array(service)
    services  

    ## @doc  list of accounts available in this application (e.g. management accounts)    
    ## @type array(account)
    accounts         

    ## @doc  list of networkservices e.g. http, ...
    ## @type array(networkservice)
    networkservices
    
    ## @doc  ip addresses linked to this application only, null if not specific to this application, link to guid of ip address as used in machine
    ## @bizz ref = cloud.machine/ipaddress
    ## @db   indexed
    ## @type array(guid)
    ipaddressguids
    
    ## @doc  list of capacity units, consumed by the application
    ## @type array(capacityunit)
    capacityunitsconsumed
    
    ## @doc  list of capacity units, provided by the application
    ## @type array(capacityunit)
    capacityunitsprovided    
  

## @doc  service offered by an application. Applications can offer various services, on different ports. 
##       Services are offered to other applications, machines, networkzones, and devices.
class service(DRPObject):

    ## @doc  flag indicating if the service is enabled
    ## @type boolean
    enabled = True

    ## @doc  remark on service    
    ## @type type_description
    description

    ## @doc  name of service
    ## @db   notnull indexed
    ## @type string
    name

    ## @doc  list of applications using this service
    ## @type array(service2application)
    services2applications              

    ## @doc  list of devices using this service    
    ## @type array(service2device)
    services2devices                   

    ## @doc  list of networkzones using this service    
    ## @type array(service2networkzone)
    services2networkzones              

    ## @doc  list of machines using this service    
    ## @type array(service2machine)
    services2machines                  

    ## @doc  list of machines using this service    
    ## @type array(service2customer)
    services2customers   
    
    ## @doc  list of lan's using this service    
    ## @type array(service2lan)
    service2lans  


## @doc  networkservice offered by an application. Applications can offer various services, on different udp or tcp ports. 
class networkservice(DRPObject):

    ## @doc  remark on service    
    ## @type type_description
    description

    ## @doc  name of service
    ## @db   notnull indexed
    ## @type string
    name    
    
    ## @doc  flag indicating if the service is enabled
    ## @type boolean
    enabled = True

    ## @doc  service must be monitored using a port check on the ports which have monitor == True
    ## @type boolean
    monitor = True

         
    ## @doc  ip addresses linked to this service only, null if not specific to this service, link to guid of ip address as used in machine
    ## @bizz ref = cloud.machine/ipaddress
    ## @db   indexed
    ## @type array(guid)
    ipaddressguids
    
    ## @doc  list of ports on which this service is available
    ## @type array(networkport)
    ports
    
class networkport(DRPObject):
   
    ## @doc  property to indicate if the port must be monitored by a monitoring tool (if the service is to be monitored) 
    ## @type boolean
    monitor = True

    ## @doc  ip protocol type (TCP/UDP)    
    ## @db   notnull indexed
    ## @type ipprotocoltype
    ipprotocoltype

    ## @doc  ip address
    ## @type type_ipaddress
    ipaddress

    ## @doc  TCP or UDP port number
    ## @type int
    portnr
    
## @doc  application using a certain service
class service2application(DRPObject):

    ## @doc  guid of the application using this service    
    ## @bizz ref = core.application/application
    ## @db   notnull indexed
    ## @type guid
    applicationguid

    ## @doc  remarks on service usage by application    
    ## @type type_description
    remark
   


# device using a certain service e.g. hardware KVM service
class service2device(DRPObject):

    ## @doc device using this service    
    ## @bizz ref = core.device/device
    ## @db   notnull indexed
    ## @type guid
    deviceguid
    
    ## @doc remarks 
    ## @type type_description
    remark

# customer using a certain service e.g. billing service
class service2customer(DRPObject):

    ## @doc customer using this service    
    ## @bizz ref = core.customer/customer
    ## @db   notnull indexed
    ## @type guid
    customerguid
    
    ## @doc remarks 
    ## @type type_description
    remark
    
    
#TODO are network zones still in drp
# networkzone using a certain service
class service2networkzone(DRPObject):
   
    ## @doc  guid of the networkzone using this service 
    ## @bizz ref = core.networkzone/networkzone
    ## @db   notnull indexed
    ## @type guid
    networkzoneguid

    ## remarks on service usage by application
    ## @type type_description
    remark
   
class service2lan(DRPObject):
   
    ## @doc  guid of the lan using this service  e.g. for portforwarding
    ## @bizz ref = core.lan/lan
    ## @db   notnull indexed
    ## @type guid
    languid

    ## remarks on service usage by application
    ## @type type_description
    remark
    
# machine using a certain service 
class service2machine(DRPObject):

    ## @doc  guid of the machine using this service    
    ## @bizz ref = core.machine/machine
    ## @db   notnull indexed
    ## @type guid
    machineguid
    
    ## @doc  remarks on service usage by application
    ## @type type_description
    remark
    

# an account in an application, e.g. management account
class account(DRPObject):

    ## @doc  login of an account for an application
    ## @db   notnull
    ## @type type_login
    login
    
    ## @doc  password of an account for an application
    ## @type type_password
    passwd
    
    ## @doc  type of the account
    ## @db   notnull indexed
    ## @type accounttype
    type    
    
   
## application status 
class statustype(QType):
    ##+ name = "ACTIVE"
    ##+ name = "DISABLED"
    ##+ name = "MAINTENANCE"

class accounttype(QType):
    ##+ name = "SYSTEMACCOUNT"
    ##+ name = "PUBLICACCOUNT"
    
 
class ipprotocoltype(QType):
    ##+ name = "UDP"
    ##+ name = "TCP"

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
    
