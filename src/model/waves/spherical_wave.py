import numpy as np

from src.utils.math import units
from src.model.waves.interface import wave
from src.model.areas.interface import area
from src.utils.optic.field import *


class SphericalWave(wave.Wave):  # todo добавить апертуру

    def __init__(self, ar: area.Area, focal_len: float, gaussian_width_param: int, wavelength: float):
        y_grid_array, x_grid_array = ar.get_coordinate_grid()
        radius_vector = np.sqrt(x_grid_array ** 2 + y_grid_array ** 2 + focal_len ** 2)
        gaussian_width_param = units.px2m(gaussian_width_param, px_size_m=ar.get_pixel_size())
        k = 2 * np.pi / wavelength

        self.__intensity = gauss_2d(x_grid_array, y_grid_array, wx=gaussian_width_param / 4, wy=gaussian_width_param / 4)
        self.__field = np.sqrt(self.__intensity) * np.exp(-1j * k * radius_vector)
        self.__wavelength = wavelength
        self.__gaussian_width_param = gaussian_width_param
        self.__focal_len = focal_len
        self.__area = ar

    @property
    def field(self):
        return self.__field

    @property
    def phase(self):
        return np.angle(self.__field)

    @property
    def intensity(self):
        return np.abs(self.__field) ** 2

    @property
    def wavelength(self):
        return self.__wavelength

    @property
    def focal_len(self):
        return self.__focal_len

    @property
    def gaussian_width_param(self):
        return int(units.m2px(self.__gaussian_width_param, self.__area.get_pixel_size()))

    @field.setter
    def field(self, field):
        self.__field = field

    @wavelength.setter
    def wavelength(self, wavelength):
        self.__wavelength = wavelength

    @gaussian_width_param.setter
    def gaussian_width_param(self, gaussian_width_param):
        self.__gaussian_width_param = gaussian_width_param

    @focal_len.setter
    def focal_len(self, focal_len):
        self.__focal_len = focal_len

    # def get_wrapped_phase(self):
    #     pass
    #
    # def get_unwrapped_phase(self):
    #     pass



