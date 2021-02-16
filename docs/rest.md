# REST API
Main interface to interact with cluster instance in order to get/add/change settings of services or nodes.

**NB!** any method that requires change of configuration may return 302 Redirect to master host if request is sent towards slave node.

# Modules:
* node - module providing access to Node configuration data
* image - module for Images manipulation
* container - module for container manipulation
* service - module for services configuration
* logs - module user for logs information(only GET method)
* vote - uses GET and UPDATE in order to handle master node election

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
    "tag": "new_one",
    "repository": "localhost"
}
</pre>

## Container
<pre>
{
    "container":"0D90B0737182",
    "image": "0D90B0737182",
    "command": "start",
    "ports": "80",
    "name": "UP"
}
</pre>
## Service
<pre>
{
    "service":"ASDFASDAF",
    "container":"",
    "replicas": 10,
    "min_replicas": 3,
    "status": "UP"
}
</pre>