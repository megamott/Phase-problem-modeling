import os
import numpy as np

from icecream import ic
from src.propagation.utils.math import units
from src.propagation.presenter.saver.saver import Saver
from src.propagation.utils.tie import FFTSolver, BoundaryConditions


# основные параметры для синтеза волны
bc = BoundaryConditions.NONE
threshold = np.exp(1) ** -2
width, height = 1024, 1024
wavelength = units.nm2m(632.8)
px_size = units.um2m(5.04)
gaussian_width_params = [250]
focal_lens = [100]
focal_lens = list(map(units.mm2m, focal_lens))

# Параметры сеток
z_shift = 1
dzs = [1]
z1_start, z1_stop = 0, 1

# параметры для формирования имени папки с данными
start = units.mm2m(0)
stop = units.mm2m(1)
step = units.mm2m(1)

for focal_len in focal_lens:
    for gaussian_width_param in gaussian_width_params:
        for dz in dzs:

            folder_name = \
                f'z_{units.m2mm(start)}-{units.m2mm(stop)}-{units.m2mm(step)} ' \
                f'f_{units.m2mm(focal_len)} ' \
                f'w_{gaussian_width_param} ' \
                f'{width}x{height}'
            saver = Saver(folder_name)

            filepath = os.path.join(os.getcwd(), os.path.pardir, os.path.pardir,
                                    'data', folder_name, 'intensity npy')

            # Создание сеток
            z2_start, z2_stop = z1_start + dz, z1_stop + dz
            z1_list = [current_z for current_z in np.arange(z1_start, z1_stop, z_shift)]
            z2_list = [current_z for current_z in np.arange(z2_start, z2_stop, z_shift)]

            for z1, z2 in zip(z1_list, z2_list):
                fn1 = os.path.join(filepath, f'z_{z1:.3f}mm.npy')
                fn2 = os.path.join(filepath, f'z_{z2:.3f}mm.npy')
                paths = [fn1, fn2]

                solver = FFTSolver(paths, dz, wavelength, px_size, bc)
                unwrapped_phase = solver.solve(threshold)
                pass

