#!/bin/bash

#TOOO:
#check in which directory

if [ "$EUID" -ne 0 ]
  then echo "Please run as sudo"
  exit
fi

if [ -z "$1" ]
  then
    echo "No argument supplied"
fi

-u www-data php /srv/www/cloud.saralon.com/htdocs/occ maintenance:mode --on
echo "\n--------------\n Server in Maintenance-Mode \n--------------\n"
-u sys.backup usr/local/bin/backup_db.sh /var/backups/backup_db
echo "\n--------------\n Database backuped \n--------------\n"
wget $1
tar -xf nextcloud*.tar.bz2
echo "\n--------------\n New Release downloaded \n--------------\n"
cp -a htdocs/.well-known nextcloud
cp -a htdocs/config nextcloud
echo "\n--------------\n Config and Extras copied \n--------------\n"
chwon -R www-data:www-data nextcloud/*
chwon root:root nextcloud
echo "\n--------------\n Ownerships changed \n--------------\n"
mv hdocs htdocs.old
mv nextcloud htdocs
echo "\n--------------\n New Version active \n--------------\n"
-u www-data php /srv/www/cloud.saralon.com/htdocs/occ upgrade
echo "\n--------------\n Datastructure upgrade \n--------------\n"
-u www-data php /srv/www/cloud.saralon.com/htdocs/occ maintenance:mode --off
echo "\n--------------\n Server not anymore in Maintenance-Mode \n--------------\n"
echo "Check now in admin overview for errors and warnigs and deal with them\n"
echo "after that is fixed run\nsudo nextcloud_deleteold.sh\n"
echo "\n--------------\n Done \n--------------\n"
