#!/bin/bash

n_its="5"  # only for the plain profiling
declare -a StringArray=("SlicePlot" "ProjectionPlot")
for plot_type in ${StringArray[@]}; do

  # time profiling
  eval "python yt_plots_profile_wrapping.py $plot_type $n_its"
  eval "gprof2dot -f pstats ${plot_type}_${n_its}.pstats | dot -Tpdf -o ${plot_type}_${n_its}_dot.pdf"
  eval "flameprof ${plot_type}_${n_its}.pstats > ${plot_type}_${n_its}_flame.svg"

  # memory profiling
  eval "python yt_plots_memray.py $plot_type"
  eval "memray flamegraph ${plot_type}_mem.bin -o ${plot_type}_mem_flame.html -f"
  eval "memray summary ${plot_type}_mem.bin  > ${plot_type}_mem_summary.txt"
  eval "memray stats ${plot_type}_mem.bin  > ${plot_type}_mem_stats.txt"
done

