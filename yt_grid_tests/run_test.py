from yt_grid_tests import build_data, functions_to_test
import argparse
import os
import shutil
import pandas as pd
from timeit import default_timer as timer
import matplotlib.pyplot as plt

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Run a test')
    parser.add_argument('ngrid_min', type=int, help="min number of grids = 2**ngrid_min")
    parser.add_argument('ngrid_max', type=int, help="max number of grids = 2**ngrid_max")
    parser.add_argument('--ngrid_type', type=str, default='power', help="if power, 2**ngrid_min:2**ngrid_max. if 'linear', range(ngrid_min, ngrid_max, ngrid_step)")
    parser.add_argument('--ngrid_step', type=int, default=1, help="if ngrid_type=='linear', ngrid_step is the increment to use")
    parser.add_argument('test_func', type=str, help="the name of the test function to run")
    parser.add_argument('--shp_exp', type=int, default=5, help='global shape will be 2**shp_exp in each dimension')
    parser.add_argument('--output_dir', type=str, default='output', help='directory for output')
    parser.add_argument('--clear_output', type=bool, default=False, help='if True, will clear output directory if it exists')
    parser.add_argument('--iters_per_test', type=int, default=1, help='number of times to run each test')

    args = parser.parse_args()
    
    if hasattr(functions_to_test, args.test_func) is False:
        raise RuntimeError(f"{args.test_func} is not a function.")

    global_shape = tuple([2**args.shp_exp for _ in range(3)])
    test_func = args.test_func

    
    if os.path.isdir(args.output_dir):
        if args.clear_output:
            shutil.rmtree(args.output_dir)
        else:
            raise RuntimeError(f"{args.output_dir} exists. Supply a new directory or set `--clear_output 1` to remove the existing files")
    os.mkdir(args.output_dir)
            
    itest = 0
    test_results = []
    for grid_exp in range(args.ngrid_min, args.ngrid_max):
        for _ in range(args.iters_per_test):
            if args.ngrid_type == 'power':
                ngrids = 2**grid_exp
            elif args.ngrid_type == 'linear':
                ngrids = args.ngrid_min + (grid_exp - args.ngrid_min) * args.ngrid_step
    
            print(f"\n\nbuilding dataset with {ngrids} grids\n\n")    
        
            # build ds from parameters
            ds = build_data.build_amr_ds_w_callable(ngrids, global_shape=global_shape)
        
            # run the test        
            test_name = os.path.join(args.output_dir, f"grid_test_{test_func}_{itest}_{ngrids}")
            func_to_call = getattr(functions_to_test, test_func)
            start = timer()
            _ = func_to_call(test_name, ds)
            end = timer()
            test_results.append({'ngrids':ngrids, 'dt_s': end-start})
            itest += 1

    df = pd.DataFrame(test_results)
    df.to_csv(os.path.join(args.output_dir, f"grid_test_{test_func}_all_results.cvs"))

    df_sum = df.groupby('ngrids')['dt_s'].agg(['std','median','mean']).reset_index()
    df_sum.to_csv(os.path.join(args.output_dir, f"grid_test_{test_func}_summary.cvs"))

    plt.plot(df_sum['ngrids'], df_sum['mean'],'k', marker='.')
    plt.plot(df_sum['ngrids'], df_sum['mean']+df_sum['std']*2,'--k', marker='.')
    plt.plot(df_sum['ngrids'], df_sum['mean']-df_sum['std']*2,'--k', marker='.')
    plt.xlabel('ngrids')
    plt.ylabel('execution time [s]')
    plt.savefig(os.path.join(args.output_dir, f"grid_test_{test_func}_summary.png"))
