from .build_data import get_data_dir
from typing import Optional, List
import os
import yt
import memray
from profilehooks import profile


class _ProfilerSettings:
    def __init__(self, profiler: str = "cprofile"):

        self.set_profiler(profiler)

    def set_profiler(self, profiler: str):
        if profiler.lower() not in ("cprofile", "memray"):
            raise ValueError("profiler must be either cProfile or memray")

        self.profiler=profiler.lower()

    def get_output_name(self, base_fn):
        # given a base filename, base_fn, modify it for a given profiler
        pfx = base_fn.replace('.', "-")
        if self.profiler == 'memray':
            return pfx+"-memray.bin"
        elif self.profiler == 'cprofile':
            return pfx + ".pstats"
        else:
            return RuntimeError("Unexpected.")


profiler_settings = _ProfilerSettings()

def find_tests(dir_for_data: Optional[str] = None,
               use_yt_data_dir: Optional[bool] = True) -> List[str]:

    dd = get_data_dir(dir_for_data=dir_for_data, use_yt_data_dir=use_yt_data_dir)

    file_list = []
    for fi in os.listdir(dd):
        if str(fi).endswith('.h5'):
            file_list.append(os.path.join(dd, fi))

    file_list.sort()
    return file_list


def _load_field(ds_container, field):
    return ds_container[field]


def get_profiled_load(pstats_file):
    @profile(filename=pstats_file, profiler="cProfile")
    def _load_a_field(ds_container, field):
        _ = _load_field(ds_container, field)

    return _load_a_field


def memray_load(output_memray_file, ds_container, field):
    with memray.Tracker(output_memray_file, native_traces=True):
        _ = _load_field(ds_container, field)


def _test_one_ds(test_file, output_stats_file):
    ds = yt.load(test_file)
    ad = ds.all_data()
    _ = ds.field_list
    field = ("all", "particle_velocity_x")

    if profiler_settings.profiler == "memray":
        memray_load(output_stats_file, ad, field)
    else:
        load_func = get_profiled_load(output_stats_file)
        load_func(ad, field)


def test_one_by_index(test_index: int,
                      output_stats_file: str,
                      dir_for_data: Optional[str] = None,
                      use_yt_data_dir: Optional[bool] = True):
    test_files = find_tests(dir_for_data, use_yt_data_dir)
    _test_one_ds(test_files[test_index], output_stats_file)

