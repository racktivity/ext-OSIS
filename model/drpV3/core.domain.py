
namespace = "core.domain"

## #doc group of backplanes, pmachines, devices & vmachines (backplanes can span multiple domains)
class domain(RootObject):

    ## @doc  description of domain (optional)
    ## @type string(60)
    description
    
    ## @doc  guid of the domain controller
    ## @bizz ref = core.application/application
    ## @db   indexed
    ## @type guid
    domaincontrollerguid
      
    ## @doc  guid of the datacenter to which the domain belongs
    ## @bizz ref = core.datacenter/datacenter
    ## @db   indexed
    ## @type guid
    datacenterguid
    
    ## @doc  list of backplanes in the domain
    ## @bizz ref = core.backplane/backplane
    ## @type array(guid)
    backplanes


    
