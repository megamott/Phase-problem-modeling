import numpy as np
from skimage.restoration import unwrap_phase

from ...model.areas.interface.aperture import Aperture
from ...model.areas.interface.area import Area
from ...model.waves.interface.wave import Wave
from ...utils.math import units
from ...utils.math.general import calc_amplitude
from ...utils.math.general import calculate_radius
from ...utils.optic.field import gauss_2d
from ...utils.optic.propagation_methods import angular_spectrum_propagation


class SphericalWave(Wave):
    """
    Волны со сферической аберрацией или сходящейся сферической волны
    """

    def __init__(self, area: Area, focal_len: float, gaussian_width_param: int, wavelength: float, distance: float):
        """
        Создание распределения поля на двухмерной координатной сетке
        :param area: двухмерная координатная сетка расчёта распределения поля
        :param focal_len: фокусное расстояние [м]
        :param gaussian_width_param: ширина гауссоиды на уровне интенсивности 1/e^2 [px]
        :param wavelength: длина волны [м]
        :param distance дистанция, на которую распространилась волна из начала координат [м]
        """

        self.__area = area
        self.__focal_len = focal_len
        self.__gaussian_width_param = gaussian_width_param
        self.__wavelength = wavelength
        self.__distance = distance

        # задание распределения интенсивности волны
        y_grid, x_grid = self.__area.coordinate_grid
        gaussian_width_param = units.px2m(gaussian_width_param, px_size_m=area.pixel_size)
        self.__intensity = gauss_2d(x_grid, y_grid,
                                    wx=gaussian_width_param / 4,
                                    wy=gaussian_width_param / 4)

        # волновой вектор
        k = 2 * np.pi / self.__wavelength
        # задание распределения комлексной амплитуды поля
        radius_vector = np.sqrt(x_grid ** 2 + y_grid ** 2 + focal_len ** 2)
        self.__field = np.sqrt(self.__intensity) * np.exp(-1j * k * radius_vector)

        # задание распределения фазы волны
        self.__phase = np.angle(self.__field)

    def get_wrapped_phase(self, aperture=None) -> np.ndarray:
        if aperture:

            # оптимизация апертуры для правильного разворачивания фазы
            # второй подоход через свёрнутую фазу
            aperture.modify_aperture(self)

            return self.__phase * aperture.aperture
        else:
            return self.__phase

    def get_unwrapped_phase(self, aperture=None):
        if aperture:

            # оптимизация апертуры для правильного разворачивания фазы
            # второй подоход через свёрнутую фазу
            aperture.modify_aperture(self)

            return unwrap_phase(self.__phase * aperture.aperture), aperture
        else:
            return unwrap_phase(self.__phase), aperture

    def get_wavefront_radius(self, aperture: Aperture) -> float:
        # развернутая фаза, обрезанная апертурой
        cut_phase, new_aperture = self.get_unwrapped_phase(aperture=aperture)

        # преобразование развернутой фазы для устранения ошибок
        # первый подход через развернутую фазу
        # mask2 = cut_phase == 0
        # cut_phase[mask2] = np.max(cut_phase)
        # cut_phase -= cut_phase.min()
        # cut_phase[mask2] = 0

        # поиск стрелки прогиба
        amplitude = calc_amplitude(cut_phase)
        sagitta = units.rad2mm(amplitude, self.__wavelength)

        # определение радиуса кривизны волнового фронта
        ap_diameter = units.m2mm(new_aperture.aperture_diameter)
        wavefront_radius = calculate_radius(sagitta, ap_diameter)

        return wavefront_radius

    def propagate_on_distance(self, z: float, method=angular_spectrum_propagation):
        method(self, z)

    @property
    def field(self) -> np.ndarray:
        return self.__field

    @field.setter
    def field(self, field):
        self.__field = field

    @property
    def area(self) -> Area:
        return self.__area

    @area.setter
    def area(self, area):
        self.__area = area

    @property
    def phase(self) -> np.ndarray:
        return np.angle(self.__field)

    @phase.setter
    def phase(self, phase):
        self.__phase = phase

    @property
    def intensity(self) -> np.ndarray:
        return np.abs(self.__field) ** 2

    @intensity.setter
    def intensity(self, intensity):
        self.__intensity = intensity

    @property
    def wavelength(self) -> float:
        return self.__wavelength

    @wavelength.setter
    def wavelength(self, wavelength):
        self.__wavelength = wavelength

    @property
    def focal_len(self) -> float:
        return self.__focal_len

    @focal_len.setter
    def focal_len(self, focal_len):
        self.__focal_len = focal_len

    @property
    def gaussian_width_param(self) -> float:
        return self.__gaussian_width_param

    @gaussian_width_param.setter
    def gaussian_width_param(self, gaussian_width_param):
        self.__gaussian_width_param = gaussian_width_param

    @property
    def distance(self) -> float:
        return self.__distance
