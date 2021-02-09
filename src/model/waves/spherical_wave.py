import numpy as np
from skimage.restoration import unwrap_phase

from src.utils.math import units
from src.model.waves.interface.wave import Wave
from src.model.areas.interface.aperture import Aperture
from src.model.areas.interface import area
from src.utils.optic.field import *
from src.utils.math.general import *


class SphericalWave(Wave):

    def __init__(self, ar: area.Area, focal_len: float, gaussian_width_param: int, wavelength: float):
        y_grid_array, x_grid_array = ar.get_coordinate_grid()
        radius_vector = np.sqrt(x_grid_array ** 2 + y_grid_array ** 2 + focal_len ** 2)
        k = 2 * np.pi / wavelength

        self.__gaussian_width_param = gaussian_width_param
        gaussian_width_param = units.px2m(gaussian_width_param, px_size_m=ar.get_pixel_size())

        self.__intensity = gauss_2d(x_grid_array, y_grid_array, wx=gaussian_width_param / 4,
                                    wy=gaussian_width_param / 4)
        self.__field = np.sqrt(self.__intensity) * np.exp(-1j * k * radius_vector)
        self.__phase = np.angle(self.__field)
        self.__wavelength = wavelength
        self.__focal_len = focal_len
        self.__area = ar

    def get_wrapped_phase(self) -> np.ndarray:
        return self.__phase

    def get_wrapped_phase_with_aperture(self, aperture: Aperture) -> np.ndarray:
        return self.__phase * aperture.get_aperture()

    def get_unwrapped_phase(self) -> np.ndarray:
        return unwrap_phase(self.__phase)

    def get_unwrapped_phase_with_aperture(self, aperture: Aperture):
        return unwrap_phase(self.__phase * aperture.get_aperture())

    def get_intensity(self) -> np.ndarray:
        return self.__intensity

    def get_wavefront_radius(self, aperture: Aperture) -> float:
        # развернутая фаза, обрезанная апертурой
        cut_phase = self.get_unwrapped_phase_with_aperture(aperture)

        # поиск стрелки прогиба
        saggita = units.rad2mm(calc_amplitude(cut_phase), self.__wavelength)

        # определение радиуса кривизны волнового фронта
        wavefront_radius = calculate_radius(saggita, units.m2mm(aperture.get_aperture_diameter()))

        return wavefront_radius

    @property
    def field(self):
        return self.__field

    @property
    def area(self):
        return self.__area

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

    # возвращает размер в пикселях
    @property
    def gaussian_width_param(self):
        return self.__gaussian_width_param

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

    @intensity.setter
    def intensity(self, intensity):
        self.__intensity = intensity

    @phase.setter
    def phase(self, phase):
        self.__phase = phase
