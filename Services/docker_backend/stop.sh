#!/usr/bin/env bash
cd /home/pi/Nakuja/n2Basestation/Services/docker_backend/

if [[ "$(docker ps -f name=nakuja -l -q)" != "" ]]
then
    make stop
else
    echo "No containers"
fi
