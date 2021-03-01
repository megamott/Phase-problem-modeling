import numpy as np
import matplotlib.pyplot as plt

from .interface.saver import Saver
from ..configuration.interface.plotter import Plotter, configuration
from ...utils.math import units


class MultiWavePlotter(Plotter):
    """
    Построение графиков для нескольких серий прогонок волн в пространстве,
    для которых волны отличаются по определенному параметру
    """

    def __init__(self, wave_array: list, aperture_array: list, distances: np.ndarray, matrix: np.ndarray, step: float,
                 saver: Saver):
        """
        :param wave_array: серии прогонок волн
        :param aperture_array: апертуры для нескольких прогонок волн
        :param distances: координаты снапшотов волн
        :param matrix: изменяющийся для прогонок параметр
        :param step: шаг прогонок
        :param saver: класс, сохраняющий волны
        """
        self.__array_wave_array = wave_array
        self.__array_aperture_array = aperture_array
        self.__z_array = distances
        self.__saver = saver
        self.__matrix = matrix
        self.__step = step

    def save_phase(self):
        ...

    def save_intensity(self):
        ...

    def save_aperture_bound(self, bound: float):
        ...

    @configuration
    def save_r_z(self, fig, ax, *args, **kwargs):
        """
        График сохранения зависимостей радиуса кривизны волнового фронта от расстояния распространения волны
        :param fig:
        :param ax:
        :param args:
        :param kwargs:
        :return:
        """
        marker = '-o'  # вид маркера линий
        markersize = kwargs.get('markersize', 2)  # размер марера линий
        linewidth = kwargs.get('linewidth', 1.)  # толщина линии графика реальных радиусов

        # определение реальных и теоретических радиусов кривизны волн и построение их графиков
        for z in np.arange(0, np.shape(self.__matrix)[0], 1):
            radius_y = []
            theory_r_z = []
            for wave, aperture, k in zip(self.__array_wave_array[z], self.__array_aperture_array[z], self.__z_array):
                radius_y.append(wave.get_wavefront_radius(aperture))
                theory_r_z.append(np.abs(np.array(k) - units.m2mm(wave.focal_len)))

            if z == 0:
                theory_r_z = np.abs(np.array(self.__z_array) - units.m2mm(self.__array_wave_array[0][0].focal_len))
                ax.plot(self.__z_array, theory_r_z,
                        label='Theoretical',
                        color='k',
                        markersize=markersize)

            ax.plot(self.__z_array, radius_y,
                    marker,
                    label=f'size: {self.__matrix[z]}',
                    linewidth=linewidth,
                    markersize=markersize)

        #  определение масштаба графиков
        theory_r_z = np.abs(np.array(self.__z_array) - units.m2mm(self.__array_wave_array[0][0].focal_len))
        ax.set_xlim(0, 500)
        ax.set_ylim(0, theory_r_z[-1])

        # заголовок графика
        plt.title(f'f\' = {units.m2mm(np.around(self.__array_wave_array[0][0].focal_len, decimals=3))} mm; '
                  f'g = {self.__array_wave_array[0][0].gaussian_width_param}; '
                  f'step = {self.__step} mm',
                  fontsize=14)
        plt.legend()

        # сохранение графиков
        package_name = 'r(z)'
        filename = f'trz_f_{int(units.m2mm(np.around(self.__array_wave_array[0][0].focal_len, decimals=3)))}_' \
                   f'g{self.__array_wave_array[0][0].gaussian_width_param}_matrix_multiple'
        self.__saver.save_image(fig, package_name, filename)

        plt.close(fig)
