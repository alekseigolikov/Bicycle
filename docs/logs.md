# Logs subsystem
Consists of 2 parts 
* REST API endpoint provided to services to raise alerts or log info
* containers logs storage
## REST API endpoints 
### Consists of 2 endpoints:
* log - endpoint to get or add log event for service
<pre>
{
    "id":"service_identity",
    "log":"Event info"
}
</pre>
* alert - endpoint to get, add or update alerts of service
<pre>
{
    "id":"service_identity",
    "state":"active, mitigated, resolved",
    "alert":"Alert info"
}
</pre>
## Log storage
### Daemon instance running on periodical basis, quering all running containers logs over docker API and storing them in json format