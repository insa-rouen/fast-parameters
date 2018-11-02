cd $HOME/Eolien/Parameters/NREL_5MW_Onshore/Wind/DLC1.1
find . -type f -name "NTM*.bts" -size 79M -exec rsync -avz --remove-source-files {} hbai@aster1.insa-rouen.fr:/home/hbai/Eolien/Parameters/NREL_5MW_Onshore/Wind/DLC1.1/ \;
