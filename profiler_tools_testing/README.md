just a test directory for trying out different profiling tools 

test scripts:

### `test_script.py`

Demonstrates standard use of the `profilehooks.profile` decorator but also how to write a wrapper to use with the decorator to easily change the decorator arguments. 

To run and then generate a dot graph:

```commandline
$ python test_script.py
$ gprof2dot -f pstats output.pstats | dot -Tpng -o output.png
```

### `yt_plots_profile_wrapping.py`

Using `profilehooks.profile` inside a wrapper so that we can vary the yt plot type that we are profiling from the command line. Will selectively profile so that we only get profile the plot command and not the dataset initialization.

To use and to generate a PDF dot graph and a flamegraph: 

```commandline
$ python yt_plots_profile_wrapping.py SlicePlot 5
$ gprof2dot -f pstats SlicePlot_5.pstats | dot -Tpdf -o SlicePlot_5_dot.pdf
$ flameprof SlicePlot_5.pstats > SlicePlot_5_flame.svg
```
the first argument to `yt_plots_profile_wrapping` is the plot type: `ProjectionPlot` or `SlicePlot` will work, would take modification to allow other plots (there are some hard coded parameters, e.g., the normal-axis and field). The second argument is the number of iterations to run. The output will sum over all iterations. 

### `yt_plots_memrary.py`

Uses memray to selectively profile just the plotting. 

To use:

```commandline
$ python yt_plots_memray SlicePlot
```
The first and only argument is the plot type (either `SlicePlot` or `ProjectionPlot`). Then use any of the `memray` commands:

```commandline
$ memray summary SlicePlot_mem.bin
$ memray stats SlicePlot_mem.bin
$ memray flamegraph SlicePlot_mem.bin
```
### `run_all_yt_plot_scripts.sh`

bash script to run all the yt plot scripts for both `ProjectionPlot` and `SlicePlot`. Will also run a bunch of commands to build all the dot and flame graphs and save some memray output.

