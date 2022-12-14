import yt
import numpy as np
from typing import Tuple, Optional
from yt.utilities.decompose import decompose_array, get_psize

def build_amr_ds_w_callable(ngrids: int, 
                            global_shape: Optional[Tuple[int, int, int]] = None,
                            bbox: Optional[np.ndarray] = None):

    # add some refinement?

    if global_shape is None:
        global_shape = (2**5, 2**5, 2**5)

    if bbox is None:
        bbox = np.array([[0., 1.], [0., 1.], [0., 1.]])


    def reader(grid, field):
        # no matter the field, we will return random
        sz = grid.ActiveDimensions
        return np.random.rand(*sz)

    grids = []
    psize = get_psize(np.array(global_shape), ngrids)
    grid_left_edges, grid_right_edges, grid_shapes, slices = decompose_array(
        global_shape, psize, bbox
    )
     

    fields = ["field0", "field1"]

    grid_data = []
    for gid in range(ngrids):
        new_grid = {
            "left_edge": grid_left_edges[gid],
            "right_edge": grid_right_edges[gid],
            "dimensions": grid_shapes[gid],
            "level": 0,
        }
        for field in fields:
            new_grid[field] = reader
    
        grid_data.append(new_grid)
    
    return yt.load_amr_grids(grid_data, global_shape, bbox=bbox)
    


