import argparse
import os
from yt_particle_tests import build_data, functions_to_test
from shutil import rmtree

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Run a test')
    big_tipsy = 'big_tipsy'
    ops = ('build_data', 'clear_data', 'list_test_range', 'test_one_by_index', big_tipsy)

    parser.add_argument('operation', type=str, help=f"the name of the test function to run: {ops}")
    parser.add_argument('--profiler', type=str, default='cProfile', help=f"The profiler to use: cProfile or memray")
    parser.add_argument('--output_dir', type=str, default='profiler_output', help=f"directory to save profiler output in")
    parser.add_argument('--use_yt_data_dir', type=bool, default=True, help="use the yt test_data_dir for on disk data")
    parser.add_argument('--dir_for_data', type=str, default="yt_fake_particle_datasets", help="the subdirectory for on disk data")
    parser.add_argument('--test_file_index', type=int, default=0,
                        help="the dataset test index (see output from list_test_range)")

    args = parser.parse_args()

    if args.operation == "build_data":
        build_data.create_test_suite_on_disk(dir_for_data=args.dir_for_data, use_yt_data_dir=args.use_yt_data_dir)
    elif args.operation == "clear_data":
        dd = build_data.get_data_dir(dir_for_data=args.dir_for_data, use_yt_data_dir=args.use_yt_data_dir)
        rmtree(dd)
    elif args.operation == "list_test_range":
        ff = functions_to_test.find_tests(dir_for_data=args.dir_for_data, use_yt_data_dir=args.use_yt_data_dir)

        ffstr = ""
        for itest, testfi in enumerate(ff):
            ffstr += f"\n{itest}: {testfi}"

        print(f"There are {len(ff)} test datasets available: \n{ffstr}")
    elif args.operation == 'test_one_by_index':
        ff = functions_to_test.find_tests(dir_for_data=args.dir_for_data, use_yt_data_dir=args.use_yt_data_dir)
        test_fi = ff[args.test_file_index]


        functions_to_test.profiler_settings.set_profiler(args.profiler)


        profiler_output_file = functions_to_test.profiler_settings.get_output_name(os.path.basename(test_fi))
        dd = build_data.get_data_dir(dir_for_data=args.dir_for_data, use_yt_data_dir=args.use_yt_data_dir)
        profiler_output_dir = os.path.join(dd, args.output_dir)
        if os.path.isdir(profiler_output_dir) is False:
            os.mkdir(profiler_output_dir)
        profiler_output_file = os.path.join(profiler_output_dir, profiler_output_file)

        print(f"testing\n {test_fi} \n\n saving to \n {profiler_output_file}")
        functions_to_test._test_one_ds(test_fi, profiler_output_file)

    elif args.operation == big_tipsy:

        functions_to_test.profiler_settings.set_profiler(args.profiler)

        out_dir = args.output_dir
        if os.path.isdir(out_dir) is False:
            os.mkdir(out_dir)
        profiler_output_file = functions_to_test.profiler_settings.get_output_name(big_tipsy)
        profiler_output_file = os.path.join(out_dir, profiler_output_file)

        functions_to_test.big_tipsy_sphere_selection(profiler_output_file)


