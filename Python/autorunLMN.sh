cd $HOME/Eolien/Parameters/NREL_5MW_Onshore/Wind/DLC1.3
find . -maxdepth 1 -name "*.bts" -size +70M -type f -exec cp {} ~/aster1/Wind/DLC1.3/ \; -exec rm {} \;
find . -maxdepth 1 -name "*.sum" -size +33k -type f -exec cp {} ~/aster1/Wind/DLC1.3/ \; -exec rm {} \;
