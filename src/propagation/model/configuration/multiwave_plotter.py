import numpy as np
import matplotlib.pyplot as plt

from .interface.saver import Saver
from ..configuration.interface.plotter import Plotter
from ...utils.math import units


class MultiWavePlotter(Plotter):
    """
    Построение графиков для нескольких серий прогонок волн в пространстве,
    для которых волны отличаются по определенному параметру
    """

    def __init__(self, wave_array: list, aperture_array: list, distances: np.ndarray, matrix: np.ndarray, saver: Saver):
        self.__array_wave_array = wave_array
        self.__array_aperture_array = aperture_array
        self.__z_array = distances
        self.__saver = saver
        self.__matrix = matrix

    def save_phase(self):
        pass

    def save_intensity(self):
        pass

    def save_aperture_bound(self, bound: float):
        pass

    def save_r_z(self, step):
        fig, ax = plt.subplots(figsize=[8.0, 6.0], dpi=300, facecolor='w', edgecolor='k')

        radius_y = []
        theory_r_z = []

        for z in np.arange(0, np.shape(self.__matrix)[0], 1):
            for wave, aperture, k in zip(self.__array_wave_array[z], self.__array_aperture_array[z], self.__z_array):
                radius_y.append(wave.get_wavefront_radius(aperture))
                theory_r_z.append(np.abs(np.array(k) - units.m2mm(wave.focal_len)))

            if z == 0:
                theory_r_z = np.abs(np.array(self.__z_array) - units.m2mm(self.__array_wave_array[0][0].focal_len))
                ax.plot(self.__z_array, theory_r_z, label='Theoretical', color='k', markersize=2)
            ax.plot(self.__z_array, radius_y, '-o', label=f'size: {self.__matrix[z]}', linewidth=1.,
                    markersize=2)
            radius_y = []
            theory_r_z = []


        theory_r_z = np.abs(np.array(self.__z_array) - units.m2mm(self.__array_wave_array[0][0].focal_len))
        ax.set_xlim(0, 500)
        ax.set_ylim(0, theory_r_z[-1])

        plt.xlabel('Propagation distance, mm')
        plt.ylabel('R(z), mm', )
        plt.legend()
        plt.title(f'f\' = {units.m2mm(np.around(self.__array_wave_array[0][0].focal_len, decimals=3))} mm; '
                  f'g = {self.__array_wave_array[0][0].gaussian_width_param}; step = {step} mm',
                  fontsize=14)
        # plt.show()

        ax.grid(True)

        package_name = 'r(z)'
        filename = f'trz_f_{int(units.m2mm(np.around(self.__array_wave_array[0][0].focal_len, decimals=3)))}_' \
                   f'g{self.__array_wave_array[0][0].gaussian_width_param}_matrix_mult'

        self.__saver.save_image(fig, package_name, filename)
