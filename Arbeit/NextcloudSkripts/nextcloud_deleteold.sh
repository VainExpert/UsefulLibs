#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as sudo"
  exit
fi

rm -rf /srv/www/cloud.saralon.com/htdocs.old
rm /srv/www/cloud.saralon.com/nextcloud*.tar.bz2
echo "\n--------------\n Removed successfully \n--------------\n"
echo "\n--------------\n Done \n--------------\n"
