#!/bin/bash

#TODO: everything with check/if

#check for available space (in GB) and not free space (in %)
#from followig commands:
df -h
echo "\n--------------\n There are $free % on nextcloud available \n--------------\n"
echo "\n--------------\n Continuing to resize storage \n--------------\n"
echo "\n--------------\n No resize needed \n--------------\n"
#/dev/mapper/vg_data-srv_nextcloud_data xxxG xxG xxxG xx% /srv/nextcloud_data
vgdisplay vg_data
echo "\n--------------\n There are $available GiB Space still available \n--------------\n"
#Free PE / Size xxxxxx / xxx,xx GiB
#if certain threshold matched (in %)
# -> resize volume with size (arbitrary if no shell parameter)
echo "\n--------------\n No size given using, Resizing with +50GB \n--------------\n"

lvresize -r -L +50G /dev/mapper/vg_data-srv_nextcloud_data
echo "\n--------------\n Succesfully resized with +50GB \n--------------\n"
echo "\n--------------\n There are $available GiB - 50GB Space still available \n--------------\n"

lvresize -r -L +$1G /dev/mapper/vg_data-srv_nextcloud_data
echo "\n--------------\n Succesfully resized with +$1 \n--------------\n"
echo "\n--------------\n There are $available GiB - $1 Space still available \n--------------\n"

echo "\n--------------\n Done \n--------------\n"
