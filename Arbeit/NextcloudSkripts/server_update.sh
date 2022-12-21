#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as sudo"
  exit
fi

apt-get update
echo -e "\n----------------------------\n Halfway There \n----------------------------\n"
apt-get dist-upgrade
echo "\n----------------------------\n Done \n----------------------------\n"
