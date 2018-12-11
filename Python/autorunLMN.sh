cd $HOME/Eolien/Parameters/NREL_5MW_Onshore/Wind/DLC1.1
find . -maxdepth 1 -name '*.bts' -size +70M -type f -exec cp {} ~/aster1/Wind/DLC1.1/ \; -exec rm {} \;
find . -maxdepth 1 -name '*.sum' -type f -exec cp {} ~/aster1/Wind/DLC1.1/ \;
