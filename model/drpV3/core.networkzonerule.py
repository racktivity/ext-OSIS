
namespace = "core.networkzonerule"


class networkzonerule(RootObject):

    ## @db   notnull indexed
    ## @bizz ref = networkzone
    ## @type guid
    sourcenetworkzoneguid
    
    ## @db   notnull indexed
    ## @bizz ref = networkzone
    ## @type guid
    destnetworkzoneguid
    
    ## @type int
    nrhops

    ## @type type_ipaddress
    gatewayip

    ## @type string
    log

    ## @type boolean
    disabled = True

    ## @type int
    freetransit

    ## @type int
    priority

    ## @type array(ipzonerule)
    ipzonerules



class ipzonerule(DRPObject):

    ## @type string(255)
    iprange

    ## @type string(40)
    portrange

    ## @type boolean
    allow = True

    ## @type string
    log

    ## @type boolean
    disabled = True

    ## @type string
    custom
