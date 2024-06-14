import yt
import pickle

if __name__ == '__main__':

    fname = 'IsolatedGalaxy/galaxy0030/galaxy0030'
    ds = yt.load(fname)

    with open('yt_ds.pickle', 'wb') as handle:
        pickle.dump(ds, handle, protocol=pickle.HIGHEST_PROTOCOL)
