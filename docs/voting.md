# Voting
Process is using Raft algorithm in order to select 
* Voting is done by senting GET request to every node on cluster from first node trigered process, causing all nodes to skip its voting prcedure untill for next configured amount of time
* result of voting request should be name of master node known to voted host with its votes ammount, which should be used by node initiated voting in order to understand network failure recovery scenario.
* Election procedure is finished by updating election with UPDATE request with results in raw body json format to every node in cluster with amount of votes gathered