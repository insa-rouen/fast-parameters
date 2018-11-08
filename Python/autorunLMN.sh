cd $HOME/Eolien/Parameters/NREL_5MW_Onshore/Wind/DLC1.1
find . -maxdepth 1 -name '*.bts' -size +70M -type f -exec cp {} ~/aster1/ \; -exec rm {} \;
