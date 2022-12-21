#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as sudo"
  exit
fi

if [ -z "$1" ]
  then
    echo "No argument supplied"
    exit
fi

if [ $PWD != "/srv/www/cloud.saralon.com" ]
  then
    echo -e "Please execute in directory /srv/www/cloud.saralon.com/"
    exit
fi

sudo -u www-data php /srv/www/cloud.saralon.com/htdocs/occ maintenance:mode --on
echo -e "\n----------------------------\n Server in Maintenance-Mode \n----------------------------\n"
sudo -u sys.backup usr/local/bin/backup_db.sh /var/backups/backup_db
echo -e "\n----------------------------\n Database backuped \n----------------------------\n"
sudo tar -czf /srv/www/cloud.saralon.com.bak.tar.gz /srv/www/cloud.saralon.com
echo -e "\n----------------------------\n Webroot of Nextcloud saved \n----------------------------\n"
sudo wget $1
sudo tar -xf nextcloud*.tar.bz2
echo -e "\n----------------------------\n New Release downloaded \n----------------------------\n"
sudo cp -a htdocs/.well-known nextcloud
sudo cp -a htdocs/config nextcloud
echo -e "\n----------------------------\n Config and Extras copied \n----------------------------\n"
sudo chown -R www-data:www-data nextcloud/*
sudo chown root:root nextcloud
echo -e "\n----------------------------\n Ownerships changed \n----------------------------\n"
sudo mv hdocs htdocs.old
sudo mv nextcloud htdocs
echo -e "\n----------------------------\n New Version active \n----------------------------\n"
sudo -u www-data php /srv/www/cloud.saralon.com/htdocs/occ upgrade
echo -e "\n----------------------------\n Datastructure upgrade \n----------------------------\n"
sudo -u www-data php /srv/www/cloud.saralon.com/htdocs/occ maintenance:mode --off
echo -e "\n----------------------------\n Server not anymore in Maintenance-Mode \n----------------------------\n"
echo -e "Check now in admin overview for errors and warnigs and deal with them\n"
echo -e "after that is fixed run\nsudo nextcloud_deleteold.sh\n"
echo -e "\n----------------------------\n Done \n----------------------------\n"
