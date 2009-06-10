namespace = "core.job"

## @doc  class that provides the properties of a job
class job(RootObject):

    ## @doc  guid of the parent job
    ## @bizz ref = core.job/job
    ## @db   indexed
    ## @type guid
    parentjobguid
    
    ## @doc  status of the job
    ##       The status is retrieved from the enumerator jobstatus
    ## @type jobstatus
    ## @db   notnull indexed
    jobstatus

    ## @doc  the date and time when the job is started
    ## @type type_date
    starttime
 
    ## @doc  the date and time when the job has finished
    ## @type type_date
    endtime
        
    ## @doc  guid of the customer who has initiated the job
    ## @bizz ref = core.customer/customer
    ## @db   indexed
    ## @type guid
    customerguid

    ## @doc  list jobsteps
    ## @type array(jobstep)
    jobsteps        
    
## @doc  show details of jobstep
class jobstep(RootObject):    
    
    ## @doc  the date and time when the jobstep is started (epoch)
    ## @type type_date
    starttime
 
    ## @doc  the date and time when the jobstep has finished (epoch)
    ## @type type_date
    endtime
    
    ## @doc  log info of jobstep
    ## @type array(logitem)
    logitems 
    
        ## @doc  status of the jobstep
    ##       The status is retrieved from the enumerator jobstepstatus
    ## @type jobstepstatus
    ## @db   notnull indexed
    status

## @doc  one logging item
class logitem(RootObject):    
    
    ## @doc  log text
    ## @type type_string
    log   
    
    ## @doc  loglevel
    ## @type loglevel
    ## @db   notnull indexed
    loglevel    
        
class loglevel(QType):  #@todo to be filled in by Kristof
    ##+ name = "MESSAGE"
    ##+ name = "DETAILEDMESSAGE"    
    ##+ name = "ERROR"
    ##+ name = "STDOUT"
    ##+ name = "STDERR"
    ##+ name = "TRACING1"
    ##+ name = "TRACING2"
    ##+ name = "TRACING3"
    ##+ name = "TRACING4"
    ##+ name = "TRACING5"
    
class jobstatus(QType):
    ##+ name = "RUNNING"
    ##+ name = "DONE"
    ##+ name = "WAITING"
    ##+ name = "ERROR"


class jobstepstatus(QType):
    ##+ name = "OK"
    ##+ name = "ERROR"
 