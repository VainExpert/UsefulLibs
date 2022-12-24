#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as sudo"
  exit
fi

sudo apt-get update
echo -e "----------------------------\n Halfway There \n----------------------------"
sudo apt-get dist-upgrade
echo "----------------------------\n Done \n----------------------------"
