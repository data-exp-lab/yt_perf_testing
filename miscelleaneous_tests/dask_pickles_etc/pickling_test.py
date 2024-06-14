import pickle
import yt


if __name__ == "__main__":
    yt.config.ytcfg.set('yt', 'store_parameter_files', True)
    yt.set_log_level(1)
    fname = 'IsolatedGalaxy/galaxy0030/galaxy0030'
    ds = yt.load(fname)
    ds.index

    ds_1 = pickle.loads(pickle.dumps(ds))
    ds_1.index