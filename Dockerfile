FROM debian:latest
MAINTAINER Mumtaz mumtaz.ahmad@siemens.com

RUN apt-get update && apt-get install -y dpkg-dev devscripts 
RUN apt-get install -y dos2unix vim s3fs openssh-server iproute2 s3fs
RUN apt-get install -y python3-texttable

CMD ["bash"]