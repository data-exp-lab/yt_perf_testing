import yt
import pickle

if __name__ == '__main__':

    with open('yt_ds.pickle', 'rb') as handle:
        ds = pickle.load(handle)

    ds.index
