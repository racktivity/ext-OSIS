
# Namespace
namespace = "core.lan"

# A lan is a logical piece of the network. It can be used to represent a subnet or an ip range
class lan(RootObject):
    
    ## @doc  optional name for lan, if empty=network, ...
    ## @db   notnull indexed
    ## @type string
    name  

    ## @doc  additional remarks / description
    ## @type type_description
    description  
   
    ## @doc  VLAN tag of this VLAN. VLAN tag 0 means that no VLAN technology is used.    
    ## @db   notnull
    ## @type int
    vlantag = 0        
    
    ## @doc  guid of the backplane on which the LAN lives
    ## @db   unique indexed
    ## @bizz ref = core.backplane/backplane
    ## @type guid
    backplaneguid
        
    ## @doc  lan's are part of one or more vdc's
    ## @bizz ref = cloud.vdc/vdc
    ## @db   indexed
    ## @type array(guid)
    vdcguids
    
    ## @doc  flag indicating if the Q-LAN has a public IP addresses or not
    ## @type boolean
    publicflag = False
    
    ## @doc  flag indicating if the Q-LAN is a management Q-LAN or not
    ## @type boolean
    managementflag = False
    
    ## @doc  flag indicating if the Q-LAN is used for storage purposes
    ##       Usually used on InfiniBand or Fibre Channel backplanes
    ## @type boolean
    storageflag = False
        
    ## @doc  subnet of the Q-LAN, e.g. 192.168.0.0
    ## @type type_networkaddress
    network
    
    ## @doc  (optional) netmask of the Q-LAN subnet, e.g. 255.255.0.0
    ## @type type_netmaskaddress
    netmask
    
    ## @doc  default gateway of the Q-LAN, e.g. 192.168.0.1
    ## @type type_ipaddress
    gateway
    
    ## @doc  start IP address, to define the IP range of the Q-LAN
    ## @type type_ipaddress
    startip
    
    ## @doc  end IP address, to define the IP range of the Q-LAN
    ## @type type_ipaddress
    endip
   
    ## @doc  link to guid of ip address as used in machine
    ## @bizz ref = cloud.machine/ipaddress
    ## @db   indexed
    ## @type array(guid)
    ipaddressguids
    
    ## @doc  guid of the parent lan (if any)
    ## @db   unique indexed
    ## @bizz ref = core.lan/lan
    ## @type guid
    parentlanguid    
 
    
    
    


   
