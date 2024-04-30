# mapt
Python tool to search debian package in multiple ubuntu/debian repositories  without changing sources.list file on host machine

### Clone repository on your host machine 
git clone https://github.com/mahmad2504/mapt.git

### Build docker image 
Change directory to folder where you have cloned the code and build docker image first

sudo docker build -t "mydebian:latest" .

### Run docker image
sudo docker run -it --rm  -w /hostdir -v ${PWD}:/hostdir mydebian  

On success you should see a bash shell terminal root@a7b6f188bfc7:/hostdir# 

### Configure repositories

Add/Update debian/ubuntu repositories in suites.json file and make sure that it is syntactically correct (u can use any online json parser to verify json data)
for example https://jsonlint.com/

Respositories are listed as array of json objects where each object represents a single repository which will be scanned (See suites.json file which is provded as sample)

Respository json objcts has following attributes

* url : http://de.archive.ubuntu.com/ubuntu/    - Public url to the respository     
* distribution : trusty                         - Distrbution Name
* components : ["main"],                        - Array of components  like main, contrib, non-free
* sources : true,                               - true means you are interested in source packages too (deb-src)
* arch : [ "i386", "amd64" ]                    - Array of architecture in which you are interested
* skip : true                                   - Optional, If set to true, this entry will be skipped by the tool



### Search a packahe
./search samba 

### Output

+---------+---------------------------------+------------------------+-------+
| Package |             Version             |         Suite          | Arch  |
+=========+=================================+========================+=======+
| samba   | 2:4.1.6+dfsg-1ubuntu2           | ubuntu:trusty          | i386  |
+---------+---------------------------------+------------------------+-------+
| samba   | 2:4.1.6+dfsg-1ubuntu2           | ubuntu:trusty          | amd64 |
+---------+---------------------------------+------------------------+-------+
| samba   | 2:4.3.11+dfsg-0ubuntu0.14.04.20 | ubuntu:trusty-security | i386  |
+---------+---------------------------------+------------------------+-------+
| samba   | 2:4.3.11+dfsg-0ubuntu0.14.04.20 | ubuntu:trusty-security | amd64 |
+---------+---------------------------------+------------------------+-------+
| samba   | 2:4.13.13+dfsg-1~deb11u5        | debian:bullseye        | i386  |
+---------+---------------------------------+------------------------+-------+
| samba   | 2:4.13.13+dfsg-1~deb11u5        | debian:bullseye        | amd64 |
+---------+---------------------------------+------------------------+-------+
![image](https://github.com/mahmad2504/mapt/assets/15646324/23e7d050-fb7d-4e8f-85bc-26e8b5b88a72)






