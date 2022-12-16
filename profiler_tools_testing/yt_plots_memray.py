# selective memory monitoring with memray
#   $ python yt_plots_memray SlicePlot
# then:
#   $ memray summary SlicePlot_mem.bin
#   $ memray stats SlicePlot_mem.bin
import yt
import memray
import sys

if __name__ == "__main__":

    # get the projection function
    plot_type = sys.argv[1]
    output_memray_file = f"{plot_type}_mem.bin"
    fld = ("enzo", "Density")
    yt_plot_func = getattr(yt, plot_type)  # plot func handle, e.g., SlicePlot
    ds = yt.load_sample("IsolatedGalaxy")
    with memray.Tracker(output_memray_file):
        # call it!
        p = yt_plot_func(ds, "x", fld)
        p.save()
