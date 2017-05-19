
# filename = './DLC2.3/DLC2.3_EOGO'
# set terminal svg enhanced mouse
# set output filename.'.svg'

# set title 'NREL 5MW Onshore : DLC 2.3 EOG v_{out}=25m/s'
# set xlabel 'time (s)'
# set ylabel 'Wind speed (m/s)'
# set y2label 'Deflection (m)'
# set ytics nomirror
# set ytics 1
# set y2tics 0.2
# set grid
# plot filename.".out" using 1:2 with line axis x1y1 title 'WindVxi: wind velocity at HH (downwind component)', filename.".out" using 1:11 with line axis x2y2 title 'TTDspFA: yaw bearing at tower-top (fore-aft deflection)'

filename = './DLC0.1/DLC0.1'
set terminal svg enhanced mouse
set output filename.'.svg'

set title 'NREL 5MW Onshore : DLC 0.1 Constant Wind Speed v^{cst}=18m/s'
set xlabel 'time (s)'
set ylabel 'Wind speed (m/s)'
set y2label 'Deflection (m)'
set ytics nomirror
# set ytics 1
set y2tics 0.2
set grid
plot filename.".out" using 1:2 with line axis x1y1 title 'WindVxi: wind velocity at HH (downwind component)', filename.".out" using 1:11 with line axis x2y2 title 'TTDspFA: yaw bearing at tower-top (fore-aft deflection)'

