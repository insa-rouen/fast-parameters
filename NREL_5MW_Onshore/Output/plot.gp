
#-----------------------------------------------------------------------------------------
#                                         DLC 0.1
# #-----------------------------------------------------------------------------------------
# filename = './DLC0.1/DLC0.1'
# set terminal postscript enhanced color
# set lmargin 4
# set rmargin 7
# set bmargin 0.1
# set tmargin 1.5
# set output '| ps2pdf - '.filename.'.pdf'

# set label center at graph 0.5,1.08 'NREL 5MW Onshore : DLC 0.1 Constant Wind Speed v^{cst}=18m/s'
# set xlabel 'time (s)'
# set ylabel 'Wind speed (m/s)'
# set y2label 'Deflection (m)'
# set ytics nomirror
# set ytics 0.2
# set yrange [17:18.8]
# set y2tics 0.2
# set grid
# plot filename.".out" using 1:2 with line axis x1y1 title 'WindVxi: wind velocity at HH (downwind component)', filename.".out" using 1:14 with line axis x2y2 title 'TTDspFA: yaw bearing at tower-top (fore-aft deflection)'

# filename = './DLC0.1/DLC0.1_InitCond'
# set terminal postscript enhanced color
# set lmargin 4
# set rmargin 7
# set bmargin 0.1
# set tmargin 1.5
# set output '| ps2pdf - '.filename.'.pdf'

# set label center at graph 0.5,1.08 'NREL 5MW Onshore : DLC 0.1 Constant Wind Speed v^{cst}=18m/s' 
# set label center at graph 0.5,1.04 '{/*0.9 Begin with an initial condition which is defined at 40^{th}s in a previous study}' 
# set xlabel 'time (s)'
# set ylabel 'Wind speed (m/s)'
# set y2label 'Deflection (m)'
# set ytics nomirror
# set ytics 0.2
# set yrange [17:18.8]
# set y2tics 0.2
# set y2range [-0.4:1.4]
# set grid
# plot filename.".out" using 1:2 with line axis x1y1 title 'WindVxi: wind velocity at HH (downwind component)', filename.".out" using 1:14 with line axis x2y2 title 'TTDspFA: yaw bearing at tower-top (fore-aft deflection)'

#-----------------------------------------------------------------------------------------
#                                         DLC 1.1
#-----------------------------------------------------------------------------------------
# filename = './DLC1.1/DLC1.1_NTM_9mps'
# set terminal postscript enhanced color
# set lmargin 4
# set rmargin 7
# set bmargin 0.1
# set tmargin 1.5
# set output '| ps2pdf - '.filename.'.pdf'

# set label center at graph 0.5,1.08 'NREL 5MW Onshore : DLC 1.1 Normal Turbulence Model v_{r}=9m/s'
# set xlabel 'time (s)'
# set xtics 60
# set ylabel 'Wind speed (m/s)'
# set y2label 'Deflection (m)'
# set ytics nomirror
# set ytics 1
# set yrange [0:14]
# set y2tics 0.2
# set y2range [-1.0:1.8]
# set grid
# plot filename.".out" using 1:2 with line axis x1y1 title 'WindVxi: wind velocity at HH (downwind component)', filename.".out" using 1:14 with line axis x2y2 title 'TTDspFA: yaw bearing at tower-top (fore-aft deflection)'


# filename = './DLC1.1/DLC1.1_NTM_19mps'
# set terminal postscript enhanced color
# set lmargin 4
# set rmargin 7
# set bmargin 0.1
# set tmargin 1.5
# set output '| ps2pdf - '.filename.'.pdf'

# set label center at graph 0.5,1.08 'NREL 5MW Onshore : DLC 1.1 Normal Turbulence Model v_{r}=19m/s'
# set xlabel 'time (s)'
# set xtics 60
# set ylabel 'Wind speed (m/s)'
# set y2label 'Deflection (m)'
# set ytics nomirror
# set ytics 1
# set yrange [5:33]
# set y2tics 0.2
# set y2range [-1.0:1.8]
# set grid
# plot filename.".out" using 1:2 with line axis x1y1 title 'WindVxi: wind velocity at HH (downwind component)', filename.".out" using 1:14 with line axis x2y2 title 'TTDspFA: yaw bearing at tower-top (fore-aft deflection)'


# filename = './DLC1.1/DLC1.1_NTM_23mps'
# set terminal postscript enhanced color
# set lmargin 4
# set rmargin 7
# set bmargin 0.1
# set tmargin 1.5
# set output '| ps2pdf - '.filename.'.pdf'

# set label center at graph 0.5,1.08 'NREL 5MW Onshore : DLC 1.1 Normal Turbulence Model v_{r}=23m/s'
# set xlabel 'time (s)'
# set xtics 60
# set ylabel 'Wind speed (m/s)'
# set y2label 'Deflection (m)'
# set ytics nomirror
# set ytics 1
# set yrange [8:36]
# set y2tics 0.2
# set y2range [-1.0:1.8]
# set grid
# plot filename.".out" using 1:2 with line axis x1y1 title 'WindVxi: wind velocity at HH (downwind component)', filename.".out" using 1:14 with line axis x2y2 title 'TTDspFA: yaw bearing at tower-top (fore-aft deflection)'

#-----------------------------------------------------------------------------------------
#                                         DLC 2.3
#-----------------------------------------------------------------------------------------
# filename = './DLC2.3/DLC2.3_EOGO'
# set terminal postscript enhanced color
# set lmargin 4
# set rmargin 7
# set bmargin 0.1
# set tmargin 1.5
# set output '| ps2pdf - '.filename.'.pdf'

# set label center at graph 0.5,1.08 'NREL 5MW Onshore : DLC 2.3 EOG v_{out}=25m/s'
# set xlabel 'time (s)'
# set ylabel 'Wind speed (m/s)'
# set y2label 'Deflection (m)'
# set ytics nomirror
# set ytics 3
# set yrange [0:33]
# set y2tics 0.2
# set grid
# plot filename.".out" using 1:2 with line axis x1y1 title 'WindVxi: wind velocity at HH (downwind component)', filename.".out" using 1:14 with line axis x2y2 title 'TTDspFA: yaw bearing at tower-top (fore-aft deflection)'


# filename = './DLC2.3/DLC2.3_EOGO_InitCond'
# set terminal postscript enhanced color
# set lmargin 4
# set rmargin 7
# set bmargin 0.1
# set tmargin 1.5
# set output '| ps2pdf - '.filename.'.pdf'

# set label center at graph 0.5,1.08 'NREL 5MW Onshore : DLC 2.3 EOG v_{out}=25m/s'
# set label center at graph 0.5,1.04 '{/*0.9 Begin with an initial condition which is defined at 40^{th}s in a previous study}'
# set xlabel 'time (s)'
# set ylabel 'Wind speed (m/s)'
# set y2label 'Deflection (m)'
# set ytics nomirror
# set ytics 3
# set yrange [0:33]
# set y2tics 0.2
# set y2range [-0.6:1.6]
# set grid
# plot filename.".out" using 1:2 with line axis x1y1 title 'WindVxi: wind velocity at HH (downwind component)', filename.".out" using 1:14 with line axis x2y2 title 'TTDspFA: yaw bearing at tower-top (fore-aft deflection)'


filename = './DLC2.3/DLC2.3_EOGO_linear'
set terminal postscript enhanced color
set lmargin 4
set rmargin 7
set bmargin 0.1
set tmargin 1.5
set output '| ps2pdf - '.filename.'.pdf'

set label center at graph 0.5,1.08 'NREL 5MW Onshore : DLC 2.3 EOG v_{out}=25m/s'
set label center at graph 0.5,1.04 '{/*0.9 Assume that wind velocity speeds up from 0 to 25m/s during 20s}'
set xlabel 'time (s)'
set ylabel 'Wind speed (m/s)'
set y2label 'Deflection (m)'
set ytics nomirror
set ytics 3
set yrange [0:33]
set y2tics 0.2
set y2range [-0.6:1.6]
set grid
plot filename.".out" using 1:2 with line axis x1y1 title 'WindVxi: wind velocity at HH (downwind component)', filename.".out" using 1:14 with line axis x2y2 title 'TTDspFA: yaw bearing at tower-top (fore-aft deflection)'

