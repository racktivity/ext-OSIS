
namespace = "core.event"

## @doc  details of an event in the datacenter
class event(RootObject):
     
    ## @doc  error code for which the event is created
    ## @type int
    errornr

    ## @doc  source for which the event is created
    ##       A source can be the Q-Shell, a script, the public SDK, ...
    ## @type string
    source

    ## @doc  backtrace of the event, used to find the cause of the error
    ## @type string
    backtrace

    ## @doc  number of occurrences of the event
    ## @type int
    count
    
    ## @doc  timestamp of the creation time and date of the event
    ## @type type_date
    timestamp
 
    ## @doc  status of the event
    ## @type eventstatus
    ## @db   notnull indexed
    eventstatus
     
    ## @doc  guid of the application for which the event is created
    ## @bizz ref = core.application/application
    ## @db   indexed
    ## @type guid
    application


    ## @doc  guid of the job for which the event is created
    ## @bizz ref = core.job/job
    ## @db   indexed
    ## @type guid
    job

    ## @doc  guid of the root job for which the event is created
    ## @bizz ref = core.job/job
    ## @db   indexed
    ## @type guid
    rootjob
    
    #@todo event type

    


class eventstatus(QType):
    ##+ name = "Reported"
 
