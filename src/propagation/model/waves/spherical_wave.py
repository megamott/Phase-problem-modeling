from typing import Tuple

import numpy as np
from skimage.restoration import unwrap_phase

from ..areas.grid import CartesianGrid
from ...model.areas.aperture import Aperture
from ...model.waves.interface.wave import Wave
from ...utils.math import units
from ...utils.math.general import calc_amplitude
from ...utils.math.general import calculate_radius
from ...utils.optic.field import gauss_2d
from ...utils.optic.propagation_methods import angular_spectrum_propagation


class SphericalWave(Wave):
    """ Волна со сферической аберрацией или сходящаяся сферическая волна """

    def __init__(self, grid: CartesianGrid, focal_len: float, gaussian_width_param: int, wavelength: float):
        """
        Создание распределения поля на двухмерной координатной сетке
        :param grid: двухмерная координатная сетка расчёта распределения поля
        :param focal_len: фокусное расстояние [м]
        :param gaussian_width_param: ширина гауссоиды на уровне интенсивности 1/e^2 [px]
        :param wavelength: длина волны [м]
        """

        self._grid = grid
        self._focal_len = focal_len
        self._gaussian_width_param = gaussian_width_param
        self._wavelength = wavelength

        # задание распределения интенсивности волны
        y_grid, x_grid = self._grid.grid
        gaussian_width_param = units.px2m(gaussian_width_param, px_size_m=grid.pixel_size)
        self._intensity = gauss_2d(x_grid, y_grid,
                                   wx=gaussian_width_param / 4,
                                   wy=gaussian_width_param / 4)

        # волновой вектор
        k = 2 * np.pi / self._wavelength
        # задание распределения комлексной амплитуды поля
        radius_vector = np.sqrt(x_grid ** 2 + y_grid ** 2 + focal_len ** 2)
        self._field = np.sqrt(self._intensity) * np.exp(-1j * k * radius_vector)

        # задание распределения фазы волны
        self._phase = np.angle(self._field)

    def get_wrapped_phase(self, *, aperture: Aperture = None, z: float = None) -> np.ndarray:
        if (aperture and z) is not None:

            # оптимизация апертуры для правильного разворачивания фазы
            aperture.modify(self, z)

            return self._phase * aperture.aperture_view
        else:
            return self._phase

    def get_unwrapped_phase(self, *, aperture: Aperture = None, z: float = None) -> Tuple[np.ndarray, Aperture]:
        if (aperture and z) is not None:

            # оптимизация апертуры для правильного разворачивания фазы
            aperture.modify(self, z)

            return unwrap_phase(self._phase * aperture.aperture_view), aperture
        else:
            return unwrap_phase(self._phase), aperture

    def get_wavefront_radius(self, *, aperture: Aperture, z: float) -> float:
        # развернутая фаза, обрезанная апертурой
        cut_phase, new_aperture = self.get_unwrapped_phase(aperture=aperture, z=z)

        # поиск стрелки прогиба
        amplitude = calc_amplitude(cut_phase)
        sagitta = units.rad2mm(amplitude, self._wavelength)

        # определение радиуса кривизны волнового фронта
        ap_diameter = units.m2mm(new_aperture.aperture_diameter)
        wavefront_radius = calculate_radius(sagitta, ap_diameter)

        return wavefront_radius

    def propagate_on_distance(self, z: float, method=angular_spectrum_propagation, **kwargs):
        method(self, z, **kwargs)

    @property
    def field(self) -> np.ndarray:
        return self._field

    @field.setter
    def field(self, field):
        self._field = field
        self._phase = np.angle(field)
        self._intensity = np.abs(field) ** 2

    @property
    def grid(self) -> CartesianGrid:
        return self._grid

    @grid.setter
    def grid(self, area):
        self._grid = area

    @property
    def phase(self) -> np.ndarray:
        return self._phase

    @phase.setter
    def phase(self, phase):
        # todo добавить перерасчет _field
        raise NotImplementedError

    @property
    def intensity(self) -> np.ndarray:
        return self._intensity

    @intensity.setter
    def intensity(self, intensity):
        # todo добавить перерасчет _field
        raise NotImplementedError

    @property
    def wavelength(self) -> float:
        return self._wavelength

    @wavelength.setter
    def wavelength(self, wavelength):
        self._wavelength = wavelength

    @property
    def focal_len(self) -> float:
        return self._focal_len

    @focal_len.setter
    def focal_len(self, focal_len):
        self._focal_len = focal_len

    @property
    def gaussian_width_param(self) -> float:
        return self._gaussian_width_param

    @gaussian_width_param.setter
    def gaussian_width_param(self, gaussian_width_param):
        self._gaussian_width_param = gaussian_width_param