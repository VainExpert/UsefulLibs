#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

freep=$(df -h | awk 'NR == 9{printf $5}' | cut -d '%' -f 1)
frees=$(df -h | awk 'NR == 9{printf $4}' | cut -d 'G' -f 1)
#/dev/mapper/vg_data-srv_nextcloud_data xxxG xxG xxxG xx% /srv/nextcloud_data
echo -e "\n--------------\n There are $freep % on the Nextcloud available \n--------------\n"

if [ $freep -lt 60 ]
  then 
    echo -e "\n--------------\n No resize needed \n--------------\n"
    echo -e "\n--------------\n Done \n--------------\n"

    exit

else 
    available=$(sudo vgdisplay vg_data | awk 'NR == 19{printf $7}')
    echo -e "\n--------------\n There are $available GiB Space still available \n--------------\n"
    #Free PE / Size xxxxxx / xxx,xx GiB

    if [ -z "$1" ]
      then
        echo -e "\n----------------------------\n No size given using, Resizing with +50GB \n----------------------------\n"
        lvresize -r -L +50G-e  /dev/mapper/vg_data-srv_nextcloud_data
        echo "\n----------------------------\n Succesfully resized with +50GB \n----------------------------\n"
        newspace=$available - 50
        newfree=$frees + 50
        echo -e "\n----------------------------\n There are $newspace GiB Space still available \n----------------------------\n"
        echo -e "\n----------------------------\n There are $newfree GB Space available on the NextCloud \n----------------------------\n"

    elif [ $1 -ge $available ]
      then
        echo -e "\n----------------------------\n Given size greater then available space, Resizing with +50GB \n----------------------------\n"
        lvresize -r -L +50G /dev/mapper/vg_data-srv_nextcloud_data
        echo -e "\n----------------------------\n Succesfully resized with +50GB \n----------------------------\n"
        newspace=$available - 50
        newfree=$frees + 50
        echo -e "\n----------------------------\n There are $newspace GiB Space still available \n----------------------------\n"
        echo -e "\n----------------------------\n There are $newfree GB Space available on the NextCloud \n----------------------------\n"

    else 
        lvresize -r -L +$1G /dev/mapper/vg_data-srv_nextcloud_data
        echo -e "\n----------------------------\n Succesfully resized with +$1 \n----------------------------\n"
        newspace=$available - $1
        newfree=$frees + $1
        echo -e "\n----------------------------\n There are $newspace GiB Space still available \n----------------------------\n"
        echo -e "\n----------------------------\n There are $newfree GB Space available on the NextCloud \n----------------------------\n"

    fi
fi

echo -e "\n----------------------------\n Done \n----------------------------\n"
