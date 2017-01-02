############################################################
# Dockerfile to run a Django-based web application
# Based on an Ubuntu Image
############################################################

# Set the base image to use to Ubuntu
FROM ubuntu:14.04

# Set the file maintainer (your name - the file's author)
MAINTAINER vivek@happay.in

ENV DOCKYARD_SRC=app
ENV DOCKYARD_SRVHOME=/app

# Update the default application repository sources list
RUN apt-get update 
RUN apt-get install -y vim
RUN apt-get install -y python-dev
RUN apt-get install -y python-pip
RUN apt-get install -y build-essential
RUN apt-get -y install wget
RUN apt-get -y install php5 libapache2-mod-php5 php5-mcrypt
RUN apt-get -y install curl libcurl3 libcurl3-dev php5-curl

RUN mkdir $DOCKYARD_SRC

COPY . $DOCKYARD_SRVHOME

RUN pip install uwsgi
RUN pip install -r $DOCKYARD_SRVHOME/requirements.txt

EXPOSE 8001 8000

WORKDIR $DOCKYARD_SRVHOME

RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
