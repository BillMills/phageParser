#!/usr/bin/env bash

apt-get update
apt-get install apt-transport-https ca-certificates -y
apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D

echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" | sudo tee /etc/apt/sources.list.d/docker.list
apt-get update

apt-cache policy docker-engine
apt-get update
apt-get install linux-image-extra-$(uname -r) linux-image-extra-virtual -y

apt-get update
apt-get install docker-engine -y
service docker start

usermod -aG docker vagrant
service docker restart

sleep 15

docker run -d --name orientdb -p 2424:2424 -p 2480:2480 -e ORIENTDB_ROOT_PASSWORD=rootpwd orientdb

docker run -d --hostname my-rabbit --name some-rabbit -p 8080:15672 -p 5672:5672 rabbitmq:3-management