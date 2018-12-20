# creat folder if it is not existant
#mkdir -p ~/aster1
#mkdir -p ~/lofims
#mkdir -p ~/lmn-cs
#mkdir -p ~/ARCHIVE

# mount aster1 disk
sshfs -o allow_other hbai@aster1.insa-rouen.fr:/home/hbai/Eolien/Parameters/NREL_5MW_Onshore ~/aster1
#sleep 5
#sshfs -o allow_other hbai@194.254.13.118:/home/hbai/Eolien/Parameters/NREL_5MW_Onshore ~/lofims
#sleep 5
#sshfs -o allow_other hbai@lmn-cs.insa-rouen.fr:/home/hbai/Eolien/Parameters/NREL_5MW_Onshore ~/lmn-cs
#sleep 5
#sshfs -o allow_other hbai@aster1.insa-rouen.fr:/ARCHIVE-1/hbai/Eolien/Parameters/NREL_5MW_Onshore ~/ARCHIVE

# to umount the remote disk
# fusermount -u ~/aster1
# fusermount -u ~/lofims
# fusermount -u ~/lmn-cs
# fusermount -u ~/ARCHIVE
