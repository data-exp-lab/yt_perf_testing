import numpy as np
from yt.testing import fake_particle_ds
from typing import Optional
import os
from dask.delayed import delayed
import dask
import yt

def get_in_mem_data(nparticles):
    nparticles = int(nparticles)
    return fake_particle_ds(npart=nparticles)

def create_tst_data_on_disk(nparticles, dir_for_data):
    ds = get_in_mem_data(nparticles)
    ad = ds.all_data()
    sfx = str(np.round(np.log10(nparticles), 2)).replace('.', '-')
    fn = os.path.join(dir_for_data, f"test-data-{sfx}")
    ad.save_as_dataset(fn, fields=ds.field_list)
    return fn + ".h5"


_n_particles_to_test = np.logspace(4, 7, 10)


def get_data_dir(dir_for_data: Optional[str]=None,
                 use_yt_data_dir: Optional[bool] = True):
    if dir_for_data is None:
        dir_for_data = "yt_fake_particle_datasets"

    if use_yt_data_dir:
        dir_for_data = os.path.join(yt.config.ytcfg.get("yt", "test_data_dir"),
                                    dir_for_data)

    return dir_for_data
def create_test_suite_on_disk(dir_for_data: Optional[str]=None,
                              use_yt_data_dir: Optional[bool] = True):

    dir_for_data = get_data_dir(dir_for_data=dir_for_data, use_yt_data_dir=use_yt_data_dir)

    if os.path.isdir(dir_for_data) is False:
        os.mkdir(dir_for_data)

    # test_data = [delayed(create_tst_data_on_disk)(npart, dir_for_data) for npart in _n_particles_to_test]
    # test_data_files = dask.compute(*test_data)
    test_data_files = []
    for npart in _n_particles_to_test:
        test_data_files.append(create_tst_data_on_disk(npart, dir_for_data))
    return test_data_files
