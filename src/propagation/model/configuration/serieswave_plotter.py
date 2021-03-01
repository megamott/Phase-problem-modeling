import matplotlib.pyplot as plt
import numpy as np

from ..configuration.interface.plotter import Plotter
from ..configuration.interface.saver import Saver
from ...utils.math import units


class SeriesWavePlotter(Plotter):
    """
    Построение графиков для серии прогонок волн в пространстве
    """

    def __init__(self, wave_array: list, aperture_array: list, distances: np.ndarray, step: float, saver: Saver):
        self.__wave_array = wave_array
        self.__aperture_array = aperture_array
        self.__z_array = distances
        self.__saver = saver
        self.__step = step

    def save_phase(self):
        pass

    def save_intensity(self):
        pass

    def save_aperture_bound(self, bound: float, **kwargs):
        title = kwargs.get('title', f'')
        dpi = kwargs.get('dpi', 300)
        line_widths = kwargs.get('linewidths', 3)
        labels = kwargs.get('labels', [])
        grid = kwargs.get('grid', True)
        x_label = kwargs.get('xlabel', 'x')
        y_label = kwargs.get('ylabel', 'y')
        y_scale = kwargs.get('yscale', 'linear')

        fig, ax = plt.subplots(figsize=[12.0, 10.0], dpi=dpi, facecolor='w', edgecolor='k')

        data = []
        for i in np.arange(0, self.__z_array.shape[0], 1):
            wave = self.__wave_array[i]
            aperture = self.__aperture_array[i]
            data.append(super()._make_aperture_bound_dependency(wave, aperture, bound))

        for i, (x, y) in enumerate(data):
            ax.plot(x[0], x[1], label=f'z: {units.m2mm(self.__z_array[i]):.1f} mm; '
                                      f'R: {self.__wave_array[i].get_wavefront_radius(self.__aperture_array[i]):.3f} mm')
            # ax.plot(y[0], y[1], label=f'D: {self.__aperture_array[i].aperture_diameter}')
            ax.plot(y[0], y[1])

        ax.legend(loc='upper right')
        ax.grid(grid)
        plt.title(f'f\' = {units.m2mm(np.around(self.__wave_array[0].focal_len, decimals=3))} mm; '
                  f'g = {self.__wave_array[0].gaussian_width_param}',
                  fontsize=14)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.yscale(y_scale)

        package_name = self.__saver.create_package_name('b')
        filename = self.__saver.create_filename(self.__wave_array[0], 'bounds')
        self.__saver.save_image(fig, package_name, filename)

        plt.close(fig)

    def save_r_z(self):
        fig, ax = plt.subplots(figsize=[8.0, 6.0], dpi=300, facecolor='w', edgecolor='k')

        radius_y = []
        theory_r_z = []

        for wave, aperture, z in zip(self.__wave_array, self.__aperture_array, self.__z_array):
            radius_y.append(wave.get_wavefront_radius(aperture))
            theory_r_z.append(np.abs(np.array(z) - units.m2mm(wave.focal_len)))

        ax.plot(self.__z_array, theory_r_z, label='Theoretical', color='k', markersize=2)
        ax.plot(self.__z_array, radius_y, '-o', label=f'size: {self.__wave_array[0].area.coordinate_grid[0].shape[0]}',
                linewidth=1.,
                markersize=2)

        ax.set_xlim(0, 500)
        ax.set_ylim(0, theory_r_z[-1])

        plt.xlabel('Propagation distance, mm')
        plt.ylabel('R(z), mm', )
        plt.legend()
        plt.title(f'f\' = {units.m2mm(np.around(self.__wave_array[0].focal_len, decimals=3))} mm; '
                  f'g = {self.__wave_array[0].gaussian_width_param}; step = {self.__step} mm',
                  fontsize=14)

        ax.grid(True)

        package_name = 'r(z)'
        filename = f'trz_f_{int(units.m2mm(np.around(self.__wave_array[0].focal_len, decimals=3)))}_' \
                   f'g{self.__wave_array[0].gaussian_width_param}_s{self.__wave_array[0].area.coordinate_grid[0].shape[0]}_matrix'

        self.__saver.save_image(fig, package_name, filename)

