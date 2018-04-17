#-----------------------------------------------------------------------------------------
#                                         DLC 2.3
#-----------------------------------------------------------------------------------------
filename = './DLC2.3_EOGO_Ramp@55s'
set terminal pdfcairo
set output filename.'_Pwr.pdf'

set title 'NREL 5MW Onshore : DLC 2.3 EOG v_{out}=25m/s'
set xlabel 'time (s)'
set ylabel 'Wind speed (m/s)'
set y2label 'Production (kW)'
set ytics nomirror
set ytics 5
set yrange [0:40]
set y2tics 1000
set y2range [0:8000]
set grid
plot filename.".out" using 1:2 with line axis x1y1 title 'WindVxi: wind velocity at HH (downwind component)', filename.".out" using 1:86 with line axis x2y2 title 'GenPwr: Electrical generator power'

# reset
# filename = './DLC2.3_EOGO_Ramp@55s'
# set terminal pdfcairo
# set output filename.'.pdf'

# set title 'NREL 5MW Onshore : DLC 2.3 EOG v_{out}=25m/s'
# set label center at graph 0.5,1.03 '{/*0.9 [Method 1] Assume that wind speeds up from 0 to 25m/s during 20s}'
# set xlabel 'time (s)'
# set ylabel 'Wind speed (m/s)'
# set y2label 'Deflection (m)'
# set xtics 5
# set ytics nomirror
# set ytics 5
# set yrange [0:40]
# set y2tics 0.2
# set y2range [-0.8:0.8]
# set grid
# plot filename.".out" using 1:2 with line axis x1y1 title 'WindVxi: wind velocity at HH (downwind component)', filename.".out" using 1:77 with line axis x2y2 title 'TwHt9TDxt: yaw bearing at tower-top (fore-aft deflection)'




