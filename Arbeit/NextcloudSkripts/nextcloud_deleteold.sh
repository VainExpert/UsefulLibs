#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as sudo"
  exit
fi

sudo rm -rf /srv/www/cloud.saralon.com/htdocs.old
sudo rm /srv/www/cloud.saralon.com/nextcloud*.tar.bz2
echo -e "----------------------------\n Removed successfully \n----------------------------"
echo -e "----------------------------\n Done \n----------------------------"
