
namespace = "core.networkzone"

class networkzone(RootObject):

    ## @doc is this network zone public to the internet ? Is informational of nature.
    ## @type bool
    public
      
    ## @bizz ref = core.datacenter/datacenter
    ## @db   indexed
    ## @type guid
    datacenterguid
    
    ## @bizz ref = networkzone
    ## @db   indexed
    ## @type guid
    parentnetworkzoneguid
 
    ## @type array(networkzonerange)
    ranges


class networkzonerange(DRPObject):

    ## @type type_ipaddress
    fromip

    ## @type type_ipaddress
    toip
