#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as sudo"
  exit
fi

if ! [[ "$1" =~ ^https://download\.nextcloud\.com/server/releases/nextcloud-([0-9]+(\.[0-9]+)+)\.tar\.bz2$ ]]
  then
    echo "Make sure you supplied a correct Download-Link for the .tar.bz2 of the official NextCloud Website"
    exit
fi

if [ $PWD != "/srv/www/cloud.saralon.com" ]
  then
    echo "Please execute in directory /srv/www/cloud.saralon.com/"
    exit
fi

sudo -u www-data php /srv/www/cloud.saralon.com/htdocs/occ maintenance:mode --on
echo -e "----------------------------\n Server in Maintenance-Mode \n----------------------------"
sudo -u sys.backup usr/local/bin/backup_db.sh /var/backups/backup_db
echo -e "----------------------------\n Database backuped \n----------------------------"
sudo tar -czf /srv/www/cloud.saralon.com.bak.tar.gz /srv/www/cloud.saralon.com
echo -e "----------------------------\n Webroot of Nextcloud saved \n----------------------------"
sudo wget $1
sudo tar -xf nextcloud*.tar.bz2
echo -e "----------------------------\n New Release downloaded \n----------------------------"
sudo cp -a htdocs/.well-known nextcloud
sudo cp -a htdocs/config nextcloud
echo -e "----------------------------\n Config and Extras copied \n----------------------------"
sudo chown -R www-data:www-data nextcloud/*
sudo chown root:root nextcloud
echo -e "----------------------------\n Ownerships changed \n----------------------------"
sudo mv hdocs htdocs.old
sudo mv nextcloud htdocs
echo -e "----------------------------\n New Version active \n----------------------------"
sudo -u www-data php /srv/www/cloud.saralon.com/htdocs/occ upgrade
echo -e "----------------------------\n Datastructure upgrade \n----------------------------"
sudo -u www-data php /srv/www/cloud.saralon.com/htdocs/occ maintenance:mode --off
echo -e "----------------------------\n Server not anymore in Maintenance-Mode \n----------------------------"
echo -e "----------------------------\nCheck now in admin overview for errors and warnings and deal with them\n"
echo -e "after that is fixed run\n> sudo nextcloud_deleteold.sh\n----------------------------"
echo -e "----------------------------\n Done \n----------------------------"
