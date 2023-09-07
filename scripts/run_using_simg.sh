#!/bin/bash
container_path=/gporq3/store_0/usr/aiidausr/SINGULARITY/containers
container_name=ai4mat-AiiDA_v.1.1.simg
module load singularity-3.5.2
cd ..
while  [ true ]
do
    singularity exec --bind /etc/krb5.conf,/etc/ssh/ssh_config,/gporq2,/gporq3,/afs/enea.it/software/qu_esp/pseudo/  $container_path/$container_name python main.py
done
