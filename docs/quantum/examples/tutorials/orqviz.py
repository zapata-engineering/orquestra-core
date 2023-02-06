import orqviz
import numpy as np

np.random.seed(42)

def cost_Function(pars):
    return np.sum(np.cos(pars))**2 + np.sum(np.sin(30*pars))**2
n_params = 42

params = np.random.uniform(-np.pi, np.pi, size=n_params)
dir1 = orqviz.geometric.get_random_normal_vector(n_params)
dir2 = orqviz.geometric.get_random_orthonormal_vector(dir1)

scan2D_result = orqviz.scans.perform_2D_scan(params, cost_Function,
                                direction_x=dir1, direction_y=dir2,
                                n_steps_x=100)
orqviz.scans.plot_2D_scan_result(scan2D_result)