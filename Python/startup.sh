# creat folder if it is not existant
mkdir -p ~/aster1
# mount aster1 disk
sleep 15
sshfs -o allow_other hbai@aster1.insa-rouen.fr:/home/hbai/Eolien/Parameters/NREL_5MW_Onshore/Wind/DLC1.1 ~/aster1
# find . -maxdepth 1 -name '*.bts' -size +70M -exec cp {} ~/aster1/ \; -exec rm {} \;
