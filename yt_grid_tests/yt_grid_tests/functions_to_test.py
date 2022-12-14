import yt


def projection_plot(test_name, ds):
    savename = f"{test_name}.png"
    p = yt.ProjectionPlot(ds, 'x', ("stream", "field0")) 
    p.save(savename)
    return True
