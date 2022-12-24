#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

freep=$(df -h | awk 'NR == 9{printf $5}' | cut -d '%' -f 1)
frees=$(df -h | awk 'NR == 9{printf $4}' | cut -d 'G' -f 1)
#/dev/mapper/vg_data-srv_nextcloud_data xxxG xxG xxxG xx% /srv/nextcloud_data
echo -e "----------------------------\n There are $freep % on the Nextcloud available \n----------------------------"

if [ $freep -lt 60 ]
  then 
    echo -e "----------------------------\n No resize needed \n----------------------------"
    echo -e "----------------------------\n Done \n----------------------------"

    exit

else 
    available=$(sudo vgdisplay vg_data | awk 'NR == 19{printf $7}')
    echo -e "----------------------------\n There are $available GiB Space still available \n----------------------------"
    #Free PE / Size xxxxxx / xxx,xx GiB

    if [ -z "$1" ]
      then
        echo -e "----------------------------\n No size given using, Resizing with +50GB \n----------------------------"
        sudo lvresize -r -L +50G-e  /dev/mapper/vg_data-srv_nextcloud_data
        echo "----------------------------\n Succesfully resized with +50GB \n----------------------------"
        newspace=$available - 50
        newfree=$frees + 50
        echo -e "----------------------------\n There are $newspace GiB Space still available \n----------------------------"
        echo -e "----------------------------\n There are $newfree GB Space available on the NextCloud \n----------------------------"

    elif [ $1 -ge $available ]
      then
        echo -e "----------------------------\n Given size greater then available space, Resizing with +50GB \n----------------------------"
        sudo lvresize -r -L +50G /dev/mapper/vg_data-srv_nextcloud_data
        echo -e "----------------------------\n Succesfully resized with +50GB \n----------------------------"
        newspace=$available - 50
        newfree=$frees + 50
        echo -e "----------------------------\n There are $newspace GiB Space still available \n----------------------------"
        echo -e "----------------------------\n There are $newfree GB Space available on the NextCloud \n----------------------------"

    else 
        sudo lvresize -r -L +$1G /dev/mapper/vg_data-srv_nextcloud_data
        echo -e "----------------------------\n Succesfully resized with +$1 \n----------------------------"
        newspace=$available - $1
        newfree=$frees + $1
        echo -e "----------------------------\n There are $newspace GiB Space still available \n----------------------------"
        echo -e "----------------------------\n There are $newfree GB Space available on the NextCloud \n----------------------------"

    fi
fi

echo -e "\n----------------------------\n Done \n----------------------------\n"
