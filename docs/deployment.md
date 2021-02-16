# Deployment subsystem
## Node scenario:
States: ADD->RUNING->STOP->STOPED->RUN->RUNING
### STATE ADD
* Creates configuration file 
* Bootstraps new node using Ansible workbook
* Uploading code to new node
* Adding daemon as service
* Running service
* Changes state of Node to RUNING
### STATE STOP
* Master node runing Ansible workbook to stop service on requested node
* Change state of Node to STOPED
### STATE RUN
* Master node runing Ansible workbook to start service on requested node
* Change state of Node to RUNING

## Image scenario:
NEW->LOCAL->REMOVE
### STATE NEW
* Local node pull image from registry
* Change state to LOCAL
### STATE REMOVE
* Prunes image locally
* Remove image recrod from DB

## Container scenario:
NEW->LOCAL->REMOVE
### STATE NEW
* Builds container localy
* Change state to LOCAL
### STATE REMOVE
* Removes container
* Removes container record from local DB

## Service scenario:
NEW-> RUNNING -> UPDATE -> RUNNING
NEW-> RUNNING -> STOP -> STOPED
RUN-> RUNNING -> STOP -> STOPED
### STATE NEW, RUN
* calculate maximum of min_instances_per_node/instances_per_active node
* generates network maping file for traffic manager
* Runing required amount of instances
* Runing Ansible workbook to change A10/F5/DNS SRV servers used in order to balance load between cluster instances
* Changes state to RUNING
### STATE RUNING is used to rebalance cluster if needed
* periodically check that votes are received from all hosts and instatnces_per_active_node requirement is met
* if not changes state to UPDATE
### STATE UPDATE
* recalculate new amount of active hosts
* regenerates network maping file for trafic manager
* Runing additional amount of instances
* Runing Ansible workbook to change trafic manager configuration
### STATE STOP
* Runing Ansible workbook to offload traffic from runing instances
* Stoping all runing instances
* Changes state of service to STOPED