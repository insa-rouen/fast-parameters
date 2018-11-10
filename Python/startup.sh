# creat folder if it is not existant
mkdir -p ~/aster1
# mount aster1 disk
sleep 15
sshfs -o allow_other hbai@aster1.insa-rouen.fr:/home/hbai/Eolien/Parameters/NREL_5MW_Onshore ~/aster1
# to umount the remote disk
# fusermount -u tmp
