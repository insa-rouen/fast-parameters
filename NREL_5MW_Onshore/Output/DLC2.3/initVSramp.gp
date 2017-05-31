# [HB]
# To compare the result that obtained by:
#   Simulation begins with a wind speed ramp
#   Simulation begins under an initial condition
# in the same figure

#-----------------------------------------------------------------------------------------
#                                         DLC 2.3
#-----------------------------------------------------------------------------------------
# !paste DLC2.3_EOGO_linear.out DLC2.3_EOGO_InitCond.out | awk '{print $1, $14, $31, $44}' > DLC2.3_EOGO_initVSlinear.out

filename = './DLC2.3_EOGO_initVSramp'
set terminal pdfcairo
set output filename.'.pdf'

set title 'NREL 5MW Onshore : DLC 2.3 EOG v_{out}=25m/s'
set label center at graph 0.5,1.03 '{/*0.9 Wind speed ramp method VS Initional condition method}' 

set xlabel 'Time (s)'
set ylabel 'Error (m)'
set y2label 'Deflection (m)'
set ytics nomirror
set ytics 0.0125
set yrange [-0.05:0.05]
set y2tics 0.2
set y2range [-0.8:0.8]
set grid
plot filename.".out" using ($1-30):2 with points pointtype 6 pointsize 0.2 axis x1y2 title 'Method 1: Wind speed ramp', filename.".out" using 3:4 with lines linewidth 1.5 linecolor "gold" axis x1y2 title 'Method 2: Under initial condition', filename.".out" using 3:($2-$4) with impulses axis x1y1 title 'Error = Method 1 - Method 2'



