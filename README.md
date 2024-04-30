# mapt
Python tool to search debian package in multiple ubuntu/debian repositories  without changing sources.list file on host machine

### Clone repository on your host machine 
git clone https://github.com/mahmad2504/mapt.git

### Build docker image 
Change directory to folder where you have cloned the code and build docker image first
sudo docker build -t "mydebian:latest" .

### Run docker image
docker run -it --rm  -w /hostdir -v ${PWD}:/hostdir mydebian  

### Configure repositories

Update debian/ubuntu rpositories in suites.json file and make sure that it is syntactically correct (u can use any online json parser to verify json data)

### Search a packahe
./search samba 

### Output
![image](https://github.com/mahmad2504/mapt/assets/15646324/23e7d050-fb7d-4e8f-85bc-26e8b5b88a72)






