from skimage.restoration import unwrap_phase

from src.utils.math import units
from src.model.waves.interface.wave import Wave
from src.model.areas.interface.aperture import Aperture
from src.model.areas.interface.area import Area
from src.utils.optic.field import *
from src.utils.math.general import *


# класс волны со сферической аберрацией или сходящейся сферической волны
class SphericalWave(Wave):

    def __init__(self, ar: Area, focal_len: float, gaussian_width_param: int, wavelength: float):
        """
        Создание распределения поля на двухмерной координатной сетке
        :param ar: двухмерная координатная сетка расчёта распределения поля
        :param focal_len: фокусное расстояние [м]
        :param gaussian_width_param: ширина гауссоиды на уровне интенсивности 1/e^2 [px]
        :param wavelength: длина волны [м]
        """
        y_grid_array, x_grid_array = ar.get_coordinate_grid()
        radius_vector = np.sqrt(x_grid_array ** 2 + y_grid_array ** 2 + focal_len ** 2)
        # волновой вектор
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

    def get_wrapped_phase(self, aperture=None) -> np.ndarray:
        if aperture:
            return self.__phase * aperture.get_aperture()
        else:
            return self.__phase

    def get_unwrapped_phase(self, aperture=None) -> np.ndarray:
        if aperture:
            return unwrap_phase(self.__phase * aperture.get_aperture())
        else:
            return unwrap_phase(self.__phase)

    def get_intensity(self) -> np.ndarray:
        return self.__intensity

    def get_wavefront_radius(self, aperture: Aperture) -> float:
        # развернутая фаза, обрезанная апертурой
        cut_phase = self.get_unwrapped_phase(aperture=aperture)

        # поиск стрелки прогиба
        saggita = units.rad2mm(calc_amplitude(cut_phase), self.__wavelength)

        # определение радиуса кривизны волнового фронта
        wavefront_radius = calculate_radius(saggita, units.m2mm(aperture.get_aperture_diameter()))

        return wavefront_radius

    def get_wavelength(self) -> float:
        return self.__wavelength

    def get_area(self) -> Area:
        return self.__area

    @property
    def field(self) -> np.ndarray:
        """
        Распределение поля волны на координатной сетке в комплексной форме
        """
        return self.__field

    @property
    def area(self) -> Area:
        """
        Координатная сетка
        """
        return self.__area

    @property
    def phase(self) -> np.ndarray:
        """
        Распределение фазы поля
        :return:
        """
        return np.angle(self.__field)

    @property
    def intensity(self) -> np.ndarray:
        """
        Распределение интенсивности поля
        :return:
        """
        return np.abs(self.__field) ** 2

    @property
    def wavelength(self) -> float:
        return self.__wavelength

    @property
    def focal_len(self) -> float:
        return self.__focal_len

    @property
    def gaussian_width_param(self) -> float:
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
