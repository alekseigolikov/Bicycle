# REST API
Main interface to interact with cluster instance in order to get/add/change settings of services or nodes.

**NB!** any method that requires change of configuration may return 302 Redirect to master host if request is sent towards slave node.

# Modules:
* state - module producing list of all components in json format
* node - module providing access to Node configuration data
* image - module for Images manipulation
* container - module for container manipulation
* service - module for services configuration
* logs - module user for logs information(only GET method)
* vote - uses GET and UPDATE in order to handle master node election
* [log](./logs.md) - uses GET and ADD methods in order to provide loging interface to runing service
* [alert](./logs.md) - uses GET, ADD, UPDATE methods in order to provider alerting interface to runing service

# Methods
All methods using receiving module name as uri in request part, and raw data in body part in json format
* ADD - Used to Add configuration of module
<pre>
ADD /node/ HTTP/1.1
Content-Type: text/plain
User-Agent: PostmanRuntime/7.26.10
Content-Length: 145
{
"name": "Node_1",
"address": "192.168.1.1",
"ssh_key": "0D90B0737182asdf0D90B0737"
} 
</pre>

* DELETE - request to mark some element for further deletition
<pre>
DELETE /node/ HTTP/1.1
Content-Type: text/plain
User-Agent: PostmanRuntime/7.26.10
Content-Length: 24
{"name":"InitialHost_1"}
</pre>
* UPDATE - method used to update elements of particular element
<pre>
UPDATE /node/ HTTP/1.1
Content-Type: text/plain
User-Agent: PostmanRuntime/7.26.10
Content-Length: 145
{
"name": "Node_1",
"address": "192.168.1.1",
"ssh_key": "0D90B0737182asdf0D90B0737"
} 

</pre>
* GET - gets json having name as parameter to list setting for particular element or does not require any to provide whole list of all elements in DB
<pre>
GET /node/ HTTP/1.1
Content-Type: text/plain
User-Agent: PostmanRuntime/7.26.10
Content-Length: 145
{
"name": "Node_1",
} 

</pre>

# Modules fields values

## Node
<pre>
{
"name": "Node_1",
"address": "192.168.1.1",
"ssh_key": "0D90B0737182asdf0D90B0737"
} 
</pre>

## Image
<pre>
{
    "image": "0D90B0737182",
    "tag": "latest",
    "repository": "localhost"
}
</pre>

## Container
<pre>
{
    "container":"0D90B0737182",
    "image": "0D90B0737182",
    "command": "start",
    "ports": "80,81,82,83,84,85,86,87,88,89,90",
    "name": "Transactions"
}
</pre>
## Service
<pre>
{
    "service":"Transactions_engine",
    "container":"Transactions",
    "replicas": 10,
    "nodes":"Node_1"
    "ports":"80,81,82,83,84,85,86,87,88,89,90"
    "min_replicas": 3,
    "status": "UP"
}
</pre>